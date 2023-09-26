/** @odoo-module **/

import { _lt } from "@web/core/l10n/translation";
import { Domain } from "@web/core/domain";
import { FormViewDialog } from "@web/views/view_dialogs/form_view_dialog";
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart, onMounted, useState } = owl;

const componentModel = "knowsystem.article";
const jsTreemodels = {
    "sections": "knowsystem.section", 
    "tags": "knowsystem.tag",
    "types": "article.custom.type",
};


export class KnowSystemJsTreeContainer extends Component {
    /*
    * Re-write to import required services and update props on the component start
    */
    setup() {
        this.state = useState({ treeData: null });
        this.orm = useService("orm");
        this.actionService = useService("action");
        this.dialogService = useService("dialog");
        this.searchString = "";
        onWillStart(async () => {
            await this._loadTreeData(this.props);
        });
        onMounted(() => {
            this.jsTreeAnchor = $("#"+this.id);
            this.jsTreeSearchInput = $("#jstr_input_" + this.id)[0];
            this._renderJsTree();
        })
    }
    /*
    * Getter for title
    */
    get title() {
        return this.props.jstreeTitle;
    }
    /*
    * Getter for id (jstree_key unique reference)
    */
    get id() {
        return this.props.jstreeId;
    }
    /*
    * The method to update jsTree data
    */
    async _loadTreeData() {
        const jstreeData = await this.orm.call(componentModel, "action_get_hierarchy", [this.id]);
        Object.assign(this.state, { treeData: jstreeData });
    }
    /*
    * The method to get context_menu options
    */
    _getJsTreeContextMenu() {
        var self = this;
        return {
            "select_node": false,
            "items": function($node) {
                const jsTreeAnchor = self.jsTreeAnchor.jstree(true);
                var resultedContextMenu = {};
                if (self.props.canCreate && (!$node.data || !$node.data.no_edit)) {
                    Object.assign(resultedContextMenu, {
                        "Create": {
                            "label": _lt("Create"),
                            "action": function (obj) {
                                $node = jsTreeAnchor.create_node($node);
                                jsTreeAnchor.edit($node);
                            }
                        },
                        "Rename": {
                            "label": _lt("Rename"),
                            "action": function (obj) { jsTreeAnchor.edit($node) }
                        },
                        "Edit": {
                            "label": _lt("Edit"),
                            "action": function (obj) { self._onEditNodeForm(jsTreeAnchor, $node, false) }
                        },
                        "Remove": {
                            "separator_before": false,
                            "separator_after": false,
                            "label": _lt("Archive"),
                            "action": function (obj) { jsTreeAnchor.delete_node($node) }
                        },                        
                    });
                }
                else {
                    Object.assign(resultedContextMenu, {
                        "Settings": {
                            "label": _lt("Settings"),
                            "action": function (obj) { self._onEditNodeForm(jsTreeAnchor, $node, true) }
                        },                        
                    });
                }
                Object.assign(resultedContextMenu, {
                    "Print": {
                        "separator_before": false,
                        "separator_after": false,
                        "label": _lt("Print"),
                        "action": function (obj) { self._onPrint(parseInt($node.id)) }
                    },
                })
                return resultedContextMenu;
            },
        };
    }
    /*
    * The method to initiate jstree
    */
    async _renderJsTree() {
        if (!this.state.treeData) {
            return 
        }
        var self = this;
        const contextMenu = this._getJsTreeContextMenu();
        const plugins = ["checkbox", "contextmenu", "search", "state"];
        if (this.props.canCreate) { plugins.push("dnd") };
        const jsTreeOptions = {
            "core" : {
                "check_callback" : function (operation, node, node_parent, node_position, more) {
                    if (operation === "move_node") {
                        if (node_parent && node_parent.data && node_parent.data.no_edit) { return false }
                        else if (node && node.data && node.data.no_edit) { return false };
                    };
                    return true
                },
                "themes": {"icons": false},
                "data": this.state.treeData,
                "multiple" : true,
            },
            "plugins" : plugins,
            "state" : { "key" : this.id },
            "checkbox" : {
                "three_state" : false,
                "cascade": "down",
                "tie_selection" : false,
            },
            "contextmenu": contextMenu,
        };
        const jsTree = this.jsTreeAnchor.jstree(jsTreeOptions);
        const jsTreeAnchor = this.jsTreeAnchor.jstree(true);
        if (this.props.canCreate) {
            this.jsTreeAnchor.on("rename_node.jstree", self, function (event, data) {
                // This also includes "create" event. Since each time created, a node is updated then
                self._onUpdateNode(jsTreeAnchor, data, false);
            });
            this.jsTreeAnchor.on("move_node.jstree", self, function (event, data) {
                self._onUpdateNode(jsTreeAnchor, data, true);
            });
            this.jsTreeAnchor.on("delete_node.jstree", self, function (event, data) {
                self._onDeleteNode(data);
            });
            this.jsTreeAnchor.on("copy_node.jstree", self, function (event, data) {
                self._onUpdateNode(jsTreeAnchor, data, true);
            });
        };
        this.jsTreeAnchor.on("state_ready.jstree", self, function (event, data) {
            self._onUpdateDomain(jsTreeAnchor);
            self.jsTreeAnchor.on("check_node.jstree uncheck_node.jstree", self, function (event, data) {
                // We register "checks" only after restoring the tree to avoid multiple checked events
                self._onUpdateDomain(jsTreeAnchor);
            })
            self.jsTreeAnchor.on("open_node.jstree", self, function (event, data) {
                // On each opening we should recalculate highlighted parents
                self._highlightParent(jsTreeAnchor, jsTreeAnchor.get_checked(), "#"+self.id);
            })
        });
    }
    /*
    * The method to calculate domain based on checks and trigger the parent search model to reload
    * For 'attributes' we need the full node info since parents will be under check
    */
    _onUpdateDomain(jsTreeAnchor) {
        const checkedTreeItems = jsTreeAnchor.get_checked(this.id == "attributes");
        this._highlightParent(jsTreeAnchor, checkedTreeItems, "#"+this.id);
        this.props.onUpdateSearch(this.id, this._getDomain(checkedTreeItems));
    }
    /*
    * The method to uncheck all nodes in the tree
    */
    _onClearJsTree() {
        const jsTreeAnchor = this.jsTreeAnchor.jstree(true);
        jsTreeAnchor.uncheck_all();
        jsTreeAnchor.save_state();
        this._onUpdateDomain(jsTreeAnchor);
    }
    /*
    * The method to get change in the search input and save it
    */
    _onSearchChange(event) {
        this.searchString = event.currentTarget.value;
    }
    /*
    * The method to execute search in jsTree
    */
    _onSearchExecute() {
        const jsTreeAnchor = this.jsTreeAnchor.jstree(true);
        jsTreeAnchor.uncheck_all();
        if (this.searchString) {
            this.jsTreeAnchor.jstree("search", this.searchString);
        }
        else {
            this.jsTreeAnchor.jstree("clear_search");
        }
        this._onUpdateDomain(jsTreeAnchor); // so unchecked leaves are reflected
    }
    /*
     * The method to manage keyup on search input > if enter then make search
    */
    _onSearchkeyUp(event) {
        if (event.keyCode === 13) {
            this._onSearchExecute();
        };
    }
    /*
     * The method to clear seach input and clear jstree search
    */
    _onSearchClear() {
        this.jsTreeSearchInput.value = "";
        this.searchString = "";
        this.jsTreeAnchor.jstree("clear_search");
    }
    /*
     * The method to trigger update of jstree node
    */
    async _onUpdateNode(jsTreeAnchor, data, position) {
        if (data.node.id === parseInt(data.node.id).toString()) {
            // node exists in tree (no need for refreshing)
            if (position) {
                // that a node move
                position = parseInt(data.position);
            };
            await this.orm.call(
                componentModel,
                "action_update_node",
                [jsTreemodels[this.id], parseInt(data.node.id), data.node, position],
            );                
        }
        else {
            // brand new node
            const newNodeId = await this.orm.call(
                componentModel,
                "action_create_node",
                [jsTreemodels[this.id], data.node],
            );
            jsTreeAnchor.set_id(data.node, newNodeId);
        }
    }
    /*
     * The method to trigger unlink of jstree node 
    */
    async _onDeleteNode(data) {
        await this.orm.call(componentModel, "action_delete_node", [jsTreemodels[this.id], parseInt(data.node.id)]);
    }
    /*
     * The method to add a new root jstree item
    */
    _onAddRootTag() {
        const jsTreeAnchor = this.jsTreeAnchor.jstree(true);
        var selectedNode = jsTreeAnchor.get_selected();
        selectedNode = jsTreeAnchor.create_node("#");
        if(selectedNode) { jsTreeAnchor.edit(selectedNode) };
    }
    /*
     * The method to open node edit form
    */
    async _onEditNodeForm(jsTreeAnchor, node, preventUpdate) {
        const modelContext = this.props.kanbanModel.rootParams.context;
        this.dialogService.add(FormViewDialog, {
            resModel: jsTreemodels[this.id],
            resId: parseInt(node.id),
            context: modelContext,
            title: _lt("Settings"),
            preventCreate: preventUpdate,
            preventEdit: preventUpdate,
            onRecordSaved: async (formRecord) => { 
                jsTreeAnchor.set_text(node, formRecord.data.name);
                if (formRecord.data.parent_id && formRecord.data.parent_id.length != 0) {
                    const newParent = formRecord.data.parent_id[0].toString();
                    if (newParent != node.parent) {
                        jsTreeAnchor.move_node(node, newParent);
                    };
                };
            },
        });
    }
    /*
    * The method to print articles linked to the specific node
    */
    async _onPrint(nodeId) {
        const actionDict = await this.orm.call(componentModel, "action_print_node", [this._getDomain([nodeId])]);
        this.actionService.doAction(actionDict);
    }
    /*
    * The method to calculate domain based on JsTree values
    */
    _getDomain(checkedTreeItems) {
        if (this.id == "sections") {
            return this._getMany2OneDomain(checkedTreeItems, "section_id");
        }
        else if (this.id == "tags") {
            return this._getMany2ManyDomain(checkedTreeItems, "tag_ids")
        }
        else if (this.id == "types") {
            return this._getMany2OneDomain(checkedTreeItems, "custom_type_id");
        };
        return []
    }
    /*
    * The method to prepare the domain for M2O 'in' domain
    */
    _getMany2OneDomain(checkedTreeItems, field) {
        const checkedIds = checkedTreeItems.map(function(checkedItem) {return parseInt(checkedItem)});
        if (checkedIds.length != 0) {
            return [[field, "in", checkedIds]];
        };
        return [];
    }
    /*
    * The method to prepare the domain for M2M 'in' domain
    */
    _getMany2ManyDomain(checkedTreeItems, field) {
        var domain = [];
        _.each(checkedTreeItems, function (checkedItem) {
            domain = Domain.or([domain, [[field, "in", parseInt(checkedItem)]]]).toList();
        });
        return domain;
    }
    /*
    * The method to highlight not selected parent nodes that have selected children
    * That's triggered when a node is selected or opened. The reason for the latter is that not loaded nodes get
    * class from state while we do not want to always iterate over those
    */
    _highlightParent(jsTreeAnchor, checkedNodes, jsSelector) {
        $(jsSelector + "* .jstr-selected-parent").removeClass("jstr-selected-parent");
        var allParentNodes = [];
        _.each(checkedNodes, function (node) {
            const thisNodeParents = jsTreeAnchor.get_path(node, false, true);
            allParentNodes = allParentNodes.concat(thisNodeParents);
        });
        allParentNodes = [... new Set(allParentNodes)];
        _.each(allParentNodes, function(nodeID) {
            $(jsSelector + " * .jstree-node#" + nodeID).addClass("jstr-selected-parent");
        });
    } 
}

KnowSystemJsTreeContainer.template = "knowsystem.KnowSystemJsTreeContainer";
