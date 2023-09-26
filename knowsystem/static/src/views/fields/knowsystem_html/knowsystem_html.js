/** @odoo-module **/

import { _lt } from "@web/core/l10n/translation";
import { device } from "web.config";
import { getRangePosition } from "@web_editor/js/editor/odoo-editor/src/utils/utils";
import { getWysiwygClass } from "web_editor.loader";
import { HtmlField } from "@web_editor/js/backend/html_field";
import { initializeTabCss } from "@knowsystem/views/fields/knowsystem_html/initialize_css";
import { loadBundle, loadJS } from "@web/core/assets";
import { toInline, getCSSRules } from "web_editor.convertInline";
const { onWillStart, useSubEnv } = owl;


function stripHistoryIds(value) {
    return value && value.replace(/\sdata-last-history-steps="[^"]*?"/, '') || value;
}

export class KnowSystemHtml extends HtmlField {
    /*
    * Re-write to introduce own services and actions
    */
    setup() {
        super.setup();
        useSubEnv({ onWysiwygReset: this._resetIframe.bind(this) });
        onWillStart(() => loadJS("/web_editor/static/lib/html2canvas.js"));
    }
    /*
    * Re-write to redefine editor options
    */
    get wysiwygOptions() {
        return {
            ...super.wysiwygOptions,
            onIframeUpdated: () => this.onIframeUpdated(),
            snippets: "knowsystem.knowsystem_snippets",
            resizable: false,
            defaultDataForLinkTools: { isNewWindow: true },
            toolbarTemplate: "knowsystem.web_editor_toolbar",
            ...this.props.wysiwygOptions,
        };
    }
    /*
    * Re-write to corectly position dynamic placeholder
    */
    positionDynamicPlaceholder(popover, position) {
        const editable = this.wysiwyg.$iframe ? this.wysiwyg.$iframe[0] : this.wysiwyg.$editable[0];
        const relativeParentPosition = editable.getBoundingClientRect();
        let topPosition = relativeParentPosition.top;
        let leftPosition = relativeParentPosition.left;
        const rangePosition = getRangePosition(popover, this.wysiwyg.options.document);
        topPosition += rangePosition.top;
        leftPosition += rangePosition.left - 14;
        popover.style.top = topPosition + "px";
        popover.style.left = leftPosition + "px";
    }
    /*
    * Re-write to avoid standard field comitting
    */
    async commitChanges({ urgent } = {}) {
        if (!this._isDirty() && !this.props.aceMode) {
            return this._pendingCommitChanges;
        };
        this._pendingCommitChanges = (async () => {
            if (this.wysiwyg && this.wysiwyg.odooEditor) {
                this.wysiwyg.odooEditor.historyPauseSteps();
                await this.wysiwyg.cleanForSave();
                await this.wysiwyg.saveModifiedImages();
                const value = this.getEditingValue();
                const lastValue = (this.props.value || "").toString();
                if (value !== null && (this.props.aceMode || (!(!lastValue && stripHistoryIds(value) === "<p><br></p>")
                        && stripHistoryIds(value) !== stripHistoryIds(lastValue)))) {
                    this.props.setDirty(false);
                    this.currentEditingValue = value;
                    await this.props.update(value, this.adaptReadonly.bind(this));
                };
                this.wysiwyg.odooEditor.historyUnpauseSteps();
                this.wysiwyg.odooEditor.historyRevertCurrentStep();
            };
        })();
        return this._pendingCommitChanges;
    }
    /*
    * The method to postprocess editable description to readonly description
    */
    async adaptReadonly() {
        const $editable = this.wysiwyg.getEditable();
        const $editorEnable = $editable.closest(".editor_enable");
        $editorEnable.removeClass("editor_enable");
        this.wysiwyg.odooEditor.observerUnactive("toInline");
        const iframe = document.createElement("iframe");
        iframe.style.height = "0px";
        iframe.style.visibility = "hidden";
        iframe.setAttribute("sandbox", "allow-same-origin");
        const clonedHtmlNode = $editable[0].closest("html").cloneNode(true);
        const clonedBody = clonedHtmlNode.querySelector("body");
        const clonedIframeTarget = clonedHtmlNode.querySelector("#iframe_target");
        clonedBody.replaceChildren(clonedIframeTarget);
        clonedHtmlNode.querySelectorAll("script").forEach(script => script.remove());
        iframe.srcdoc = clonedHtmlNode.outerHTML;
        const iframePromise = new Promise((resolve) => { iframe.addEventListener("load", resolve) });
        document.body.append(iframe);
        await iframePromise;
        const editableClone = iframe.contentDocument.querySelector(".note-editable");
        this.cssRules = this.cssRules || getCSSRules($editable[0].ownerDocument);
        await toInline($(editableClone), this.cssRules, $(iframe));
        iframe.remove();
        this.wysiwyg.odooEditor.observerActive("toInline");
        const inlineHtml = editableClone.innerHTML;
        $editorEnable.addClass("editor_enable");
        const result = await this._unWrap(inlineHtml)
        return result
    }
    /*
    * Re-write to load own snippets
    */
    async startWysiwyg(...args) {
        await super.startWysiwyg(...args);
        await loadBundle({
            jsLibs: [
                "/knowsystem/static/src/wysiwyg/link_dialog_fix.js",
                "/knowsystem/static/src/wysiwyg/knowsystem_snippets.js",
            ],
        });
        await this._resetIframe();
    }
    /*
     *  Re-write to update iframe 
    */
    async _resetIframe() {
        await this._onSnippetsLoaded();
        this.wysiwyg.$iframeBody.find(".o_layout").addBack().data("name", "KnowSystem");
        this.wysiwyg.$iframeBody.find(".odoo-editor-editable").removeClass("o_editable");
        initializeTabCss(this.wysiwyg.getEditable());
        this.wysiwyg.getEditable().find("img").attr("loading", "");
        this.wysiwyg.odooEditor.observerFlush();
        this.wysiwyg.odooEditor.historyReset();
        this.wysiwyg.$iframeBody.addClass("knowsystem_iframe");
        this.onIframeUpdated();
    }
    /*
    * The method to define sidebar styles and actions (including full & mobile views)
    */
    async _onSnippetsLoaded() {
        if (this.wysiwyg.snippetsMenu && $(window.top.document).find(".o_knowsystem_form")[0]) {
            this.wysiwyg.snippetsMenu.$scrollable = this.wysiwyg.$el.closestScrollable();
            this.wysiwyg.snippetsMenu.$scrollable.css("overflow-y", "scroll");
        };
        const $snippetsSideBar = this.wysiwyg.snippetsMenu.$el;
        const $snippets = $snippetsSideBar.find(".oe_snippet");
        const selectorToKeep = ".o_we_external_history_buttons, .knowsystem_top_actions";
        $snippetsSideBar.find(`.o_we_website_top_actions > *:not(${selectorToKeep})`).attr("style", "display: none!important");
        if (device.isMobile) {
            $snippetsSideBar.hide();
            this.wysiwyg.$iframe.attr("style", "padding-left: 0px !important");
        }
        await this.wrapContainer();
        this.wysiwyg.$iframeBody.find(".iframe-utils-zone").removeClass("d-none");
    }
    /*
    * The method to wrap new article in the suitable for mailings and partially printing styles
    */
    async wrapContainer() {
        const $layout = this.wysiwyg.$iframeBody.find(".o_layout");
        let $knowsystemWrapper = $layout.children(".knowsystem_wrapper");
        let $knowsystemWrapperContent = $knowsystemWrapper.find(".knowsystem_wrapper_td");
        if (!$knowsystemWrapperContent.length) {
            $knowsystemWrapperContent = $knowsystemWrapper;
        }
        let value;
        if ($knowsystemWrapperContent.length > 0) { value = $knowsystemWrapperContent.html() } 
        else if ($layout.length) { value = $layout.html() } 
        else { value = this.wysiwyg.getValue() }
        let blankEditable = "<p><br></p>";
        const editableAreaIsEmpty = value === "" || value === blankEditable;
        if (editableAreaIsEmpty) {
            const $newWrapper = $("<div/>", { class: "container knowsystem_wrapper knowsystem_regular oe_unremovable" });
            const $newWrapperContent = $("<div/>", {
                class: "col knowsystem_no_options knowsystem_wrapper_td bg-white oe_structure o_editable"
            });
            $newWrapper.append($('<div class="row"/>').append($newWrapperContent));
            const $newLayout = $("<div/>", {
                class: "o_layout knowsystem_layout oe_unremovable oe_unmovable",
                "data-name": "KnowSystem",
            }).append($newWrapper);
            this.wysiwyg.odooEditor.resetContent($newLayout[0].outerHTML);

            $newWrapperContent.find('*').addBack()
                .contents()
                .filter(function () {
                    return this.nodeType === 3 && this.textContent.match(/\S/);
                }).parent().addClass('o_default_snippet_text');
            initializeTabCss(this.wysiwyg.$editable);
            this.wysiwyg.trigger('reload_snippet_dropzones');
            this.onIframeUpdated();
            this.wysiwyg.odooEditor.historyStep(true);
            this._switchingTheme = true;
            await this.commitChanges();
            this._switchingTheme = false;
            const $editable = this.wysiwyg.$editable.find(".o_editable");
            this.$editorMessageElements = $editable
                .not("[data-editor-message]")
                .attr("data-editor-message", this.env._t("DRAG BUILDING BLOCKS HERE"));
            $editable.filter(":empty").attr("contenteditable", false);
            setTimeout(() => {
                this.wysiwyg.historyReset();
                const document = this.wysiwyg.odooEditor.document;
                const selection = document.getSelection();
                const p = this.wysiwyg.odooEditor.editable.querySelector("p");
                if (p) {
                    const range = document.createRange();
                    range.setStart(p, 0);
                    range.setEnd(p, 0);
                    selection.removeAllRanges();
                    selection.addRange(range);
                }
            }, 0);
        }
    }
    /*
    * Initiate own wysiwyg instance
    */
    async _getWysiwygClass() {
        return getWysiwygClass({moduleName: "knowsystem.wysiwyg"});
    }
    /*
    * Re-write to trigger our commit
    */
    async _onWysiwygBlur() {
        await this.commitChanges();
    }
}

KnowSystemHtml.props = { ...HtmlField.props, aceMode: { type: Boolean, optional: true } };
KnowSystemHtml.displayName = _lt("Article");
