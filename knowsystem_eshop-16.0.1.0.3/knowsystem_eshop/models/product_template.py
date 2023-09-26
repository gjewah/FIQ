#coding: utf-8

from markupsafe import Markup

from odoo import _, fields, models

from odoo.tools.safe_eval import safe_eval


class product_template(models.Model):
    """
    Overwrite to establish direct link between products and articles
    """
    _inherit = "product.template"

    knowsystem_by_attribute_ids = fields.One2many("knowsystem.by.attribute", "template_id", string="KnowSystem FAQ")
    never_show_faq = fields.Boolean(string="Do not show eCommerce FAQ")

    def action_return_faq(self, combination, website_id):
        """
        The method to find all articles related to this product template and chosen attribute values

        Args:
         * combination - list - of ints - ids of product.attribute.values under consideration
         * website_id - website object

        Methods:
         * action_get_published_name

        Returns:
         * dict of
          ** name - string - name of the template
          ** action_type - string - "link"/"popup"
          ** article_ids - knowsystem.article recordset for portal link, and dict of article values for popup
          ** res_articles_ids - list of ints (found article ids)

        Extra info:
         * critical: security rights for tags do not obligatory equal their articles inside. So we should do everything
           under sudo, and then make search under normal search
        """
        under_user_self = self
        self = self.sudo()
        # globally applied faqs
        faq_type = website_id.knowsystem_eshop_type
        section_ids = website_id.knowsystem_faq_section_ids
        tag_ids = website_id.knowsystem_faq_tag_ids
        article_ids = website_id.knowsystem_faq_article_ids
        # template faqs (at the end we would exclude ones that do not satisfy the values)
        faq_ids = self.knowsystem_by_attribute_ids
        # attribute faqs
        chosen_attr_values = self.env["product.attribute.value"]
        if combination:
            chosen_templ_values = self.env["product.template.attribute.value"].browse(combination).exists()
            if chosen_templ_values:
                chosen_attr_values = chosen_templ_values.mapped("product_attribute_value_id")
                for attr_value in chosen_attr_values:
                    attribute_id = attr_value.attribute_id
                    for faq in attribute_id.knowsystem_by_attribute_ids:
                        # there might only one attribute value for a give attribute
                        if not faq.value_ids or attr_value in faq.value_ids:
                            faq_ids += faq
        # exclude template faqs which do not satisfy faqs
        for faq in self.knowsystem_by_attribute_ids:
            if faq.value_ids and (faq.value_ids & chosen_attr_values) != faq.value_ids:
                faq_ids -= faq
        # cumulate all crtiria settings
        if faq_ids:
            section_ids += faq_ids.mapped("section_ids")
            tag_ids += faq_ids.mapped("tag_ids")
            article_ids += faq_ids.mapped("article_ids")
        if section_ids:
            sections_with_children = self.env["knowsystem.section"].search([("id", "child_of", section_ids.ids)])
            article_ids += sections_with_children.mapped("article_ids")
        if tag_ids:
            tags_with_children = self.env["knowsystem.tag"].search([("id", "child_of", tag_ids.ids)])
            article_ids += tags_with_children.mapped("article_ids")
        # switch to the original user
        res_articles = under_user_self.env["knowsystem.article"].search([("id", "in", article_ids.ids)])
        fin_articles = res_articles
        if website_id.knowsystem_eshop_type == "popup":
            fin_articles = res_articles.mapped(lambda art: {
                "id": art.id,
                "name": art.action_get_published_name(),
                "body": art.description_arch and art.description_arch.startswith("<p><br></p>") \
                    and art.description_arch[11:] or art.description_arch or "",
            })
        return {
            "name": self.name,
            "action_type": faq_type,
            "article_ids": fin_articles,
            "res_articles_ids": res_articles.ids,
        }

    def return_faq_button(self, website_id):
        """
        The method to define whether FAQ entry should be shown. And if so, what should ne used as entry

        Args:
         * website_id - website object

        Returns:
         * str - button content
         * False if FAQ should not be shown

        Extra info:
         * Expected singleton
        """
        result = False
        eshop_type = website_id.knowsystem_eshop_type
        if website_id and not self.never_show_faq and eshop_type and eshop_type != "no":
            button_text = website_id.knowsystem_faq_style or _("<i class='fa fa-info-circle'> </i> FAQ")
            result = Markup(button_text)
        return result

