odoo.define('knowsystem.snippets_editor', function (require) {
'use strict';
/** implemented based on Odoo mass_mailing **/

    const snippetsEditor = require('web_editor.snippet.editor');

    const KnowSystemSnippetsMenu = snippetsEditor.SnippetsMenu.extend({
        custom_events: _.extend({}, snippetsEditor.SnippetsMenu.prototype.custom_events, {
            drop_zone_over: '_onDropZoneOver',
            drop_zone_out: '_onDropZoneOut',
            drop_zone_start: '_onDropZoneStart',
            drop_zone_stop: '_onDropZoneStop',
        }),
        /**
         * @override
         */
        start: function () {
            return this._super(...arguments).then(() => {
                this.$editable = this.options.wysiwyg.getEditable();
            });
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @override
         */
        _insertDropzone: function ($hook) {
            const $hookParent = $hook.parent();
            const $dropzone = this._super(...arguments);
            $dropzone.attr('data-editor-message', $hookParent.attr('data-editor-message'));
            $dropzone.attr('data-editor-sub-message', $hookParent.attr('data-editor-sub-message'));
            return $dropzone;
        },
        /**
         * @override
         */
        _updateRightPanelContent: function ({content, tab}) {
            this._super(...arguments);
            this.$('.o_we_customize_design_btn').toggleClass('active', tab === this.tabs.DESIGN);
        },

        //--------------------------------------------------------------------------
        // Handler
        //--------------------------------------------------------------------------

        /**
         * @override
         */
        _onDropZoneOver: function () {
            this.$editable.find('.o_editable').css('background-color', '');
        },
        /**
         * @override
         */
        _onDropZoneOut: function () {
            const $oEditable = this.$editable.find('.o_editable');
            if ($oEditable.find('.oe_drop_zone.oe_insert:not(.oe_vertical):only-child').length) {
                $oEditable[0].style.setProperty('background-color', 'transparent', 'important');
            }
        },
        /**
         * @override
         */
        _onDropZoneStart: function () {
            const $oEditable = this.$editable.find('.o_editable');
            if ($oEditable.find('.oe_drop_zone.oe_insert:not(.oe_vertical):only-child').length) {
                $oEditable[0].style.setProperty('background-color', 'transparent', 'important');
            }
        },
        /**
         * @override
         */
        _onDropZoneStop: function () {
            const $oEditable = this.$editable.find('.o_editable');
            $oEditable.css('background-color', '');
            if (!$oEditable.find('.oe_drop_zone.oe_insert:not(.oe_vertical):only-child').length) {
                $oEditable.attr('contenteditable', true);
            }
        },
        /**
         * @override
         */
        _onSnippetRemoved: function () {
            this._super(...arguments);
            const $oEditable = this.$editable.find('.o_editable');
            if (!$oEditable.children().length) {
                $oEditable.empty(); // remove any superfluous whitespace
                $oEditable.attr('contenteditable', false);
            }
        },
    });

    return KnowSystemSnippetsMenu;

});
