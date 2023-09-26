/** @odoo-module **/
/* @see also mass_mailing/js/mailing_mailing_view_form_full_width */

import { FormController } from "@web/views/form/form_controller";
import { throttleForAnimation } from "@web/core/utils/timing";
import { useService } from "@web/core/utils/hooks";
const { useSubEnv, onMounted, onWillUnmount } = owl;


export class KnowSystemFormController extends FormController {
    /*
    * Re-write to introduce our own actions and services
    */
    setup() {
        super.setup();
        this.actionService = useService("action");
        useSubEnv({ onIframeUpdated: () => this._updateIframe() });
        this._resizeObserver = new ResizeObserver(throttleForAnimation(() => {
            this._resizeKnowSystemEditorIframe();
            this._repositionKnowSystemEditorSidebar();
        }));
        onMounted(() => {
            $(".o_content").on(
                "scroll.repositionKnowSystemEditorSidebar", 
                throttleForAnimation(this._repositionKnowSystemEditorSidebar.bind(this))
            );
        });
        onWillUnmount(() => {
            $(".o_content").off(".repositionKnowSystemEditorSidebar");
            this._resizeObserver.disconnect();
        });
    }
    /*
    * Re-write to avoid showing translation alerts
    */
    get translateAlert() {
        return null
    }
    /*
    * The method to properly resize description widget
    */
    _updateIframe() {
        const $iframe = $("iframe.wysiwyg_iframe:visible, iframe.o_readonly");
        if (!$iframe.length || !$iframe.contents().length) { return };
        const hasIframeChanged = $iframe !== this.$iframe;
        const $oldIframe = $iframe;
        this.$iframe = $iframe;
        this._resizeKnowSystemEditorIframe();
        const $iframeDoc = $iframe.contents();
        const iframeTarget = $iframeDoc.find("#iframe_target");
        if (hasIframeChanged) {
            if ($oldIframe && $oldIframe.length && $oldIframe.contents().length) {
                // fix the bug of double toggle full screen
                $oldIframe.contents().find("body").off("click", ".o_fullscreen_btn")
            };
            $iframeDoc.find("body").on("click", ".o_fullscreen_btn", this._onToggleFullscreen.bind(this));
            if (iframeTarget[0]) {
                this._resizeObserver.disconnect();
                this._resizeObserver.observe(iframeTarget[0]);
            };
        };
        if (iframeTarget[0]) {
            const isFullscreen = this._isFullScreen();
            iframeTarget.css({
                display: isFullscreen ? "" : "flex",
                "flex-direction": isFullscreen ? "" : "column",
            });
        };
    }
    /*
    * The method to make sidebar fit the layout and make it as big as possible
    */
    _repositionKnowSystemEditorSidebar() {
        if (!this.$iframe || !this.$iframe.length || !this.$iframe.contents().length) { return };
        const windowHeight = $(window).height();
        const $iframeDocument = this.$iframe.contents();
        const $sidebar = $iframeDocument.find("#oe_snippets");
        const isFullscreen =  this._isFullScreen();
        if (isFullscreen) {
            $sidebar.height(windowHeight);
            this.$iframe.height(windowHeight);
            $sidebar.css({top: "", bottom: ""});
        } else {
            const iframeTop = this.$iframe.offset().top;
            $sidebar.css({
                height: "",
                top: Math.max(0, $(".o_content").offset().top - iframeTop),
                bottom: this.$iframe.height() - windowHeight + iframeTop,
            });
        }
    }
    /*
    * The method to make sidebar scrollable in the full width
    */
    _onToggleFullscreen() {
        if (!this.$iframe || !this.$iframe.length || !this.$iframe.contents().length) { return };
        const $iframeDoc = this.$iframe.contents();
        const html = $iframeDoc.find("html").get(0);
        html.scrollTop = 0;
        html.classList.toggle("o_fullscreen");
        const isFullscreen = this._isFullScreen();
        const wysiwyg = $iframeDoc.find(".note-editable").data("wysiwyg");
        if (wysiwyg && wysiwyg.snippetsMenu) {
            this._$scrollable = this._$scrollable || wysiwyg.snippetsMenu.$scrollable;
            wysiwyg.snippetsMenu.$scrollable = isFullscreen ? $iframeDoc.find(".note-editable") : this._$scrollable;
        }
        this._repositionKnowSystemEditorSidebar();
        this._resizeKnowSystemEditorIframe();
    }
    /*
    * The method to define whether the backend builder is in full screen    
    */
    _isFullScreen() {
        return window.top.document.body.classList.contains("o_field_widgetTextHtml_fullscreen");
    }
    /*
    * The method to make the backend editor height fits its content
    */
    _resizeKnowSystemEditorIframe() {
        if (!this.$iframe || !this.$iframe.length || !this.$iframe.contents().length) { return };
        const minHeight = $(window).height() - Math.abs(this.$iframe.offset().top);
        const $iframeDoc = this.$iframe.contents();
        const ref = $iframeDoc.find("#iframe_target")[0];
        if (ref) {
            this.$iframe.css({
                height: this._isFullScreen() ? $(window).height() : Math.max(ref.scrollHeight, minHeight),
            });
        }
    }
    /*
    * The method to launch the template selection wizard and open the new article form
    */
    async createFromTeplate() {
        const { root } = this.model;
        await this.actionService.doAction("knowsystem.create_from_template_action", { additionalContext: root.context });
    }
}

KnowSystemFormController.template = `knowsystem.KnowSystemFormView`;
