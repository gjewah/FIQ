# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

EMPTYHTML = [False, "", " ", "<p><br></p>", "<p></p>", "<p> </p>"]


class knowsystem_node(models.AbstractModel):
    """
    This is the Abstract Model to manage jstree nodes
    It is used for sections, tags, and types
    """
    _name = "knowsystem.node"
    _description = "KnowSystem Node"

    @api.constrains("parent_id")
    def _check_node_recursion(self):
        """
        Constraint for recursion
        """
        if not self._check_recursion():
            raise ValidationError(_("It is not allowed to make recursions!"))
        return True

    def _inverse_active(self):
        """
        Inverse method for active. There 2 goals:
         1. If a parent is not active, we activate it. It recursively activate all its further parents
         2. Deacticate all children. It will invoke deactivation recursively of all children after
        """
        for node in self:
            if node.active:
                # 1
                if node.parent_id and not node.parent_id.active:
                    node.parent_id.active = True
            else:
                # 2
                node.child_ids.write({"active": False})

    name = fields.Char(string="Name", required=True, translate=False)
    description = fields.Html(string="Section Description", translate=False)
    active = fields.Boolean(string="Active", default=True, inverse=_inverse_active)
    sequence = fields.Integer(string="Sequence", default=0)

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        """
        Re-write to add 'copy' in the title
        """
        if default is None:
            default = {}
        if not default.get("name"):
            default["name"] = _("%s (copy)") % (self.name)
        return super(knowsystem_node, self).copy(default)

    def name_get(self):
        """
        Overloading the method, to reflect parent's name recursively
        """
        result = []
        for node in self:
            name = "{}{}".format(node.parent_id and node.parent_id.name_get()[0][1] + "/" or "", node.name)
            result.append((node.id, name))
        return result

    @api.model
    def _return_nodes(self):
        """
        The method to return nodes in jstree format

        Methods:
         * _return_nodes_recursive

        Returns:
         * list of folders dict with keys:
           ** id
           ** text - folder_name
           ** children - array with the same keys

        Extra info:
         * here we loop over nodes without parents and do not check others, since security rights do not assume
           the situation when a user can access child without accessing parent (except website, where we rely upon
           return_nodes_with_restriction)
         * only knowsystem.section assume edit rights with restriction and only KnowSystem editors, so we calculate
           edit options only for that 
        """
        nodes = self.search([("parent_id", "=", False)])
        edit_nodes = None
        if self._name == "knowsystem.section":
            this_user = self.env.user
            if this_user.has_group("knowsystem.group_knowsystem_editor") \
                    and not self.env.user.has_group("knowsystem.group_knowsystem_admin"):
                edit_nodes = self.search([
                    "|", ("edit_global", "=", True), ("edit_access_user_ids", "in", [this_user.id])
                ])
        res = []
        for node in nodes:
            res.append(node._return_nodes_recursive(edit_nodes=edit_nodes))
        return res

    def _return_nodes_with_restriction(self, tooltip=False):
        """
        The method to return nodes in recursion for that actual nodes. Not for all

        Methods:
         * _return_nodes_recursive

        Returns:
         * list of folders dict with keys:
           ** id
           ** text - folder_name
           ** children - array with the same keys
        """
        self = self.with_context(show_tooltip=tooltip) 
        nodes = self.search([
            ("id", "in", self.ids), "|", ("parent_id", "=", False), ("parent_id", "not in", self.ids),
        ])
        res = []
        for node in nodes:
            res.append(node._return_nodes_recursive(restrict_nodes=self))
        return res

    def _return_nodes_recursive(self, restrict_nodes=False, edit_nodes=None):
        """
        The method to go by all nodes recursively to prepare their list in js_tree format

        Args:
         * nodes - optional param to restrict child with current nodes

        Extra info:
         * sorted needed to fix unclear bug of zero-sequence element placed to the end
         * Expected singleton
        """
        res = {"text": self.name, "id": self.id}
        if self._context.get("show_tooltip") and hasattr(self, "description") and self.description not in EMPTYHTML:
            res.update({"a_attr": {"kn_tip": self.description}})
        if edit_nodes is not None:
            res.update({"data": {"no_edit": self not in edit_nodes}})
        child_res = []
        child_ids = self.search([("id", "in", self.child_ids.ids)], order="sequence")
        for child in child_ids:
            if restrict_nodes and child not in restrict_nodes:
                continue
            child_res.append(child._return_nodes_recursive(restrict_nodes=restrict_nodes, edit_nodes=edit_nodes))
        res.update({"children": child_res})
        return res

    @api.model
    def create_node(self, data):
        """
        The method to update node name

        Methods:
         * _order_node_after_dnd

        Returns:
         * int - id of newly created record
        """
        name = data.get("text")
        parent_id = data.get("parent")
        if parent_id == "#":
            parent_id = False
        new_node_vals = {"name": name, "parent_id": parent_id}
        new_node = self.create([new_node_vals])
        new_node._order_node_after_dnd(parent_id=parent_id, position=False)
        return new_node.id

    def update_node(self, data, position):
        """
        The method to update node name

        Args:
         * data - dict of node params
         * position - false (in case it is rename) or int (in case it is move)

        Methods:
         * _order_node_after_dnd

        Returns:
         * int - id of udpated record

        Extra info:
         * Expected singleton
        """
        new_name = data.get("text")
        new_parent_id = data.get("parent")
        new_parent_id = new_parent_id != "#" and int(new_parent_id) or False
        if self.name != new_name:
            self.name = new_name
        if self.parent_id.id != new_parent_id:
            self.parent_id = new_parent_id
        if position is not False:
            self._order_node_after_dnd(parent_id=new_parent_id, position=position)
        return self.id

    def delete_node(self):
        """
        The method to deactivate a node
        It triggers recursive deactivation of children

        Returns:
         * int - id of udpated record

        Extra info:
         * Expected singleton
        """
        self.active = False
        return True

    def _order_node_after_dnd(self, parent_id, position):
        """
        The method to normalize sequence when position of Node has been changed based on a new element position and
        its neighbours.
         1. In case of create we put element always to the end
         2. We try to update all previous elements sequences in case it become the same of a current one (sequence
            migth be negative)

        Args:
         * parent_id - int - id of node
         * position - int or false (needed to the case of create)

        Extra info:
         * Epected singleton
        """
        the_same_children_domain = [("id", "!=", self.id)]
        if parent_id:
            the_same_children_domain.append(("parent_id.id", "=", parent_id))
        else:
            the_same_children_domain.append(("parent_id", "=", False))
        this_parent_nodes = self.search(the_same_children_domain)
        if position is False:
            position = len(this_parent_nodes)
        if this_parent_nodes:
            neigbour_after = len(this_parent_nodes) > position and this_parent_nodes[position] or False
            neigbour_before = position > 0 and this_parent_nodes[position-1] or False
            sequence = False
            if neigbour_after:
                sequence = neigbour_after.sequence - 1
                # 1
                while neigbour_before and neigbour_before.sequence == sequence:
                    neigbour_before.sequence = neigbour_before.sequence - 1
                    position -= 1
                    neigbour_before = position > 0 and this_parent_nodes[position-1] or False
            elif neigbour_before:
                sequence = neigbour_before.sequence + 1
            if sequence is not False:
                self.sequence = sequence


    # def action_website_publish(self):
    #     """
    #     The method to publish node
    #     """
    #     try:
    #         self.write({"website_published": True})
    #     except:
    #         # to the case when "website_published" is not defined
    #         pass

    # def action_website_unpublish(self):
    #     """
    #     The method to publish node
    #     """
    #     try:
    #         self.write({"website_published": False})
    #     except:
    #         pass
