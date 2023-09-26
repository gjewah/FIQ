/** @odoo-module **/

import { qweb } from "web.core";
import rpc from "web.rpc";
import publicWidget from "web.public.widget";
import "website_sale.website_sale";
import { Markup } from "web.utils";

const keys = { 37: 1, 38: 1, 39: 1, 40: 1 };
const wheelEvent = "onwheel" in document.createElement("div") ? "wheel" : "mousewheel";


publicWidget.registry.WebsiteSale.include({
    xmlDependencies: ["/knowsystem_eshop/static/src/faq_popup/faq_popup.xml"],
    events: _.extend({}, publicWidget.registry.WebsiteSale.prototype.events || {}, {
        "click .knowsystem_show_faq": "_onShowFaq",
        "click #close_faq": "_onCloseFAQ",
        "keydown": "_onKeypPressfaq",
        "keydown #faq_popup": "_onKeypPressfaq",
        "keydown #faq_body": "_onKeypPressfaq",
    }),
    /*
    * The method to show FAQ (either in the popup or open a new window)
    */
    async _onShowFaq(ev) {
        var self = this;
        event.preventDefault();
        event.stopPropagation();
        const TemplateID = parseInt(this.$(".knowsystem_show_faq")[0].id);
        const faqDict = await rpc.query({
            route: "/shop/knowsystem_faq", params: { template_id: TemplateID, attr_values: this.mainAtrrValues },
        });
        if (faqDict.action_type == "link") {
            window.location = "/knowsystem?product_faq=" + faqDict.res_articles_ids + "&product_faq_name=" + encodeURIComponent(faqDict.name);
        }
        else {
            const template = qweb.render("faqPopup", {"article_ids": faqDict.article_ids, "markup_utils": Markup});
            if (this.$("#faq_popup").length == 0) {
                const toolTipdDiv = document.createElement("div");
                const blockDiv = document.createElement("div");
                toolTipdDiv.setAttribute("id", "faq_popup");
                toolTipdDiv.setAttribute("class", "row");
                toolTipdDiv.innerHTML = template;
                $("#faq_container").after(toolTipdDiv);
                blockDiv.setAttribute("id", "faq_block");
                $("#faq_container").after(blockDiv);
                this.$el.on("click", "#faq_block", ev => this._onCloseFAQ(ev));
                this.$el.on("keydown", "#faq_block", ev => this.preventDefaultForScrollKeys(ev));
                this.$el.on("touchmove", "#faq_block", ev => this.makePreventDefault(ev));
                this.$el.on("DOMMouseScroll", "#faq_block", ev => this.makePreventDefault(ev));
                this.$el.on("wheelEvent", "#faq_block", ev => this.makePreventDefault(ev));
                $("html,body").animate({scrollTop: 1}, 100); // to move the screen start
            };
        };
    },
    /*
    * The method to prevent default actions
    */
    makePreventDefault: function(ev) {
        ev.preventDefault();
        ev.stopPropagation();
    },
    /*
    * The method to block frozen div from scrolling
    * @see https://stackoverflow.com/questions/4770025/how-to-disable-scrolling-temporarily
    */
    preventDefaultForScrollKeys: function(e) {
        if (event.key === "Escape") { this._onCloseFAQ(ev)}
        else if (keys[e.keyCode]) {
            preventDefault(e);
            return false;
        }
    },
    /*
    * Overwrite to save chosen attribute values
    */
    getSelectedVariantValues: function ($container) {
        const values = this._super(...arguments);
        if ($container.hasClass("js_main_product")) { this.mainAtrrValues = values };
        return values
    },
    /*
     * The method to remove FAQ popup
    */
    _onCloseFAQ: function(ev) {
        const faqPopup = this.$("#faq_popup");
        const blockDiv = this.$("#faq_block");
        if (faqPopup.length != 0) { faqPopup.remove() };
        if (blockDiv.length != 0) { blockDiv.remove() };
    },
    /*
     * Escape should also close FAQ popup
    */
    _onKeypPressfaq: function(ev) {
        if (event.key === "Escape") {this._onCloseFAQ(ev) }
    },
});
