odoo.define("knowsystem.snippets.options", function (require) {
"use strict";
/** implemented based on Odoo mass_mailing **/

    const options = require("web_editor.snippets.options");

    /*
    * Option to resize snippets
    */
    options.registry["sizing_knowsystem_x"] = options.Class.extend({
        start: function () {
            var def = this._super.apply(this, arguments);
            this.containerWidth = this.$target.parent().closest("td, table, div").width();
            var self = this;
            var offset, sib_offset, target_width, sib_width;
            this.$overlay.find(".o_handle.e, .o_handle.w").removeClass("readonly");
            this.isIMG = this.$target.is("img");
            if (this.isIMG) {
                this.$overlay.find(".o_handle.w").addClass("readonly");
            }
            var $body = $(this.ownerDocument.body);
            this.$overlay.find(".o_handle").on("mousedown", function (event) {
                event.preventDefault();
                var $handle = $(this);
                var compass = false;
                _.each(["n", "s", "e", "w"], function (handler) {
                    if ($handle.hasClass(handler)) { compass = handler; }
                });
                if (self.isIMG) { compass = "image"; }
                $body.on("mousemove.knowsystem_width_x", function (event) {
                    event.preventDefault();
                    offset = self.$target.offset().left;
                    target_width = self.get_max_width(self.$target);
                    if (compass === "e" && self.$target.next().offset()) {
                        sib_width = self.get_max_width(self.$target.next());
                        sib_offset = self.$target.next().offset().left;
                        self.change_width(event, self.$target, target_width, offset, true);
                        self.change_width(event, self.$target.next(), sib_width, sib_offset, false);
                    };
                    if (compass === "w" && self.$target.prev().offset()) {
                        sib_width = self.get_max_width(self.$target.prev());
                        sib_offset = self.$target.prev().offset().left;
                        self.change_width(event, self.$target, target_width, offset, false);
                        self.change_width(event, self.$target.prev(), sib_width, sib_offset, true);
                    };
                    if (compass === "image") {
                        self.change_width(event, self.$target, target_width, offset, true);
                    };
                });
                $body.one("mouseup", function () {
                    $body.off(".knowsystem_width_x");
                });
            });
            return def;
        },
        change_width: function (event, target, target_width, offset, grow) {
            target.css("width", Math.round(grow ? (event.pageX - offset) : (offset + target_width - event.pageX)));
            this.trigger_up("cover_update");
        },
        get_int_width: function (el) {
            return parseInt($(el).css("width"), 10);
        },
        get_max_width: function ($el) {
            return this.containerWidth - _.reduce(_.map($el.siblings(), this.get_int_width), function (memo, w) { return memo + w; });
        },
        onFocus: function () {
            this._super.apply(this, arguments);
            if (this.$target.is("td, th")) {
                this.$overlay.find(".o_handle.e, .o_handle.w").toggleClass("readonly", this.$target.siblings().length === 0);
            }
        },
    });

});
