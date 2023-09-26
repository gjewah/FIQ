odoo.define("knowsystem.wysiwyg", function (require) {
"use strict";
/** implemented based on Odoo mass_mailing/js/wysiwyg **/

    var Wysiwyg = require("web_editor.wysiwyg");
    const { closestElement } = require("@web_editor/js/editor/odoo-editor/src/OdooEditor");
    const KnowSystemSnippetsMenu = require("knowsystem.snippets_editor");

    const KnowsystemWysiwyg = Wysiwyg.extend({
        /*
        * Overwrite to prevent selection change outside of snippets
        */
        startEdition: async function () {
            const res = await this._super(...arguments);
            this.$editable.on("mousedown", e => {
                if ($(e.target).is(".o_editable:empty") || e.target.querySelector(".o_editable")) {
                    e.preventDefault();
                }
            });
            return res;
        },
        /*
        * Overwrite to have its own snippets editor
        */
        _createSnippetsMenuInstance: function (options={}) {
            return new KnowSystemSnippetsMenu(this, Object.assign({
                wysiwyg: this,
                selectorEditableArea: ".o_editable",
            }, options));
        },
        /*
        * The method to adapt inline commands for the backend builders
        */
        _getPowerboxOptions: function () {
            const options = this._super();
            const {commands} = options;
            const linkCommands = commands.filter(command => command.name === "Link" || command.name === "Button");
            for (const linkCommand of linkCommands) {
                linkCommand.callback = () => this.toggleLinkTools({forceDialog: false});
                const superIsDisabled = linkCommand.isDisabled;
                linkCommand.isDisabled = () => {
                    if (superIsDisabled && superIsDisabled()) {
                        return true;
                    } else {
                        const selection = this.odooEditor.document.getSelection();
                        const range = selection.rangeCount && selection.getRangeAt(0);
                        return !!range && !!closestElement(range.startContainer, "[style*=background-image]");
                    }
                }
            };
            return { ...options, commands };
        },
        /*
        * The method to hide the create-link button if the selection is within background-image.
        */
         _updateEditorUI: function (e) {
            this._super(...arguments);
            const selection = this.odooEditor.document.getSelection();
            const range = selection.rangeCount && selection.getRangeAt(0);
            const isWithinBackgroundImage = !!range && !!closestElement(range.startContainer, "[style*=background-image]");
            if (isWithinBackgroundImage) {
                this.toolbar.$el.find("#create-link").toggleClass("d-none", true);
            };
        },
    });

    return KnowsystemWysiwyg;

});
