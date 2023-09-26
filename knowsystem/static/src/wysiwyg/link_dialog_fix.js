odoo.define('knowsystem.fix.LinkDialog', function (require) {
'use strict';
/** implemented based on Odoo mass_mailing **/

    const LinkDialog = require('wysiwyg.widgets.LinkDialog');

    LinkDialog.include({
        start() {
            const ret = this._super(...arguments);
            if (!$(this.editable).find('.knowsystem_wrapper').length) {
                return ret;
            };
            this.opened().then(() => {
                this.__realMMColors = {};
                const $previewArea = $('<div/>').addClass('knowsystem_snippet_general');
                $(this.editable).find('.o_layout').append($previewArea);
                _.each(['link', 'primary', 'secondary'], type => {
                    const $el = $('<a href="#" class="btn btn-' + type + '"/>');
                    $el.appendTo($previewArea);
                    this.__realMMColors[type] = {
                        'border-color': $el.css('border-top-color'),
                        'background-color': $el.css('background-color'),
                        'color': $el.css('color'),
                    };
                    $el.remove();

                    this.$('label > .o_btn_preview.btn-' + type)
                        .css(_.pick(this.__realMMColors[type], 'background-color', 'color'));
                });
                $previewArea.remove();
                this._adaptPreview();
            });

            return ret;
        },
        _adaptPreview() {
            this._super(...arguments);
            if (this.__realMMColors) {
                var $preview = this.$("#link-preview");
                $preview.css('border-color', '');
                $preview.css('background-color', '');
                $preview.css('color', '');
                _.each(['link', 'primary', 'secondary'], type => {
                    if ($preview.hasClass('btn-' + type) || type === 'link' && !$preview.hasClass('btn')) {
                        $preview.css(this.__realMMColors[type]);
                    }
                });
            }
        },
    });

});
