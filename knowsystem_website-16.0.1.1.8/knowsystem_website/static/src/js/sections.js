/** @odoo-module **/

import { ComponentWrapper } from "web.OwlCompatibility";
import { Markup } from "web.utils";
import publicWidget from "web.public.widget";
import rpc from "web.rpc";
const { Component, useState, xml } = owl;

/*
* The method to get the current URL hash parameter
*/
function getParameterByName(parameter) {
    const currentUrl = window.location.href;
    parameter = parameter.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + parameter + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(currentUrl);
    if (!results) return "";
    if (!results[2]) return "";
    return decodeURIComponent(results[2].replace(/\+/g, " "));
};
/*
* The method to update the current param of the the URL
*/
function setParameterByName(parameter, parameterValue) {
    var url = window.location.href;
    const pattern = new RegExp("\\b(" + parameter + "=).*?(&|#|$)");
    if (url.search(pattern)>=0) {
        return url.replace(pattern,"$1" + parameterValue + "$2");
    };
    url = url.replace(/[?#]$/, "");
    return url + (url.indexOf("?")>0 ? "&" : "?") + parameter + "=" + parameterValue;
};
/*
* The method to apply page reloading based on JsTree checks
*/
function reloadTreeSearch(jstreeAnchor, parameter) {
    const jsTreeObject = jstreeAnchor.jstree(true);
    const checkedItems = jsTreeObject.get_checked();
    const currentItemsStr = getParameterByName(parameter);
    var checkedItemsStr = "";
    if (checkedItems.length != 0) { 
        checkedItemsStr = checkedItems.join(",");
        if (!checkedItemsStr) { checkedItemsStr = "" };
    };
    if (currentItemsStr != checkedItemsStr) {
        window.location = setParameterByName(parameter, checkedItemsStr);
    };
};
/*
* The method to highlight unchecked nodes that have checked children
*/
async function highlightParent(jsTreeAnchor, checkedNodes, jsSelector) {
    $(jsSelector + "* .jstr-selected-parent").removeClass("knowsystem-website-selected-parent");
    var allParentNodes = [];
    _.each(checkedNodes, function (node) {
        const thisNodeParents = jsTreeAnchor.get_path(node, false, true);
        allParentNodes = allParentNodes.concat(thisNodeParents);
    });
    allParentNodes = [... new Set(allParentNodes)];
    _.each(allParentNodes, function(nodeID) {
        $(jsSelector + " * .jstree-node#" + nodeID).addClass("knowsystem-website-selected-parent");
    });
};
/*
* The method to add item events for hovering Jstree items
*/
function addJSTreeToolTip() {
    $("a.jstree-anchor").on("mouseover", function(event) {
        const knowToolTip = event.currentTarget.getAttribute("kn_tip");
        if (knowToolTip) {
            const anchorID = event.currentTarget.getAttribute("id") + "_tooltip";
            const toolTipdDiv = document.createElement("div");
            toolTipdDiv.setAttribute("id", anchorID);
            event.currentTarget.setAttribute("remove_tool_tip", anchorID);
            toolTipdDiv.innerHTML = knowToolTip;
            toolTipdDiv.setAttribute("class", "knowsystem-website-tooltip");
            event.currentTarget.after(toolTipdDiv);
        }
    });
    $("a.jstree-anchor").on("mouseout", function(event) {
        const relateToolTip = event.currentTarget.getAttribute("remove_tool_tip");
        if (relateToolTip) {$("div#"+relateToolTip).remove()};
    });
};
/*
* The method to trigger jsTree onloading
*/
function initiateJsTree(jsTreeId, parameter) {
    $("#"+jsTreeId).each(function (index) {
        const self = $(this);
        self.jstree("destroy");
        const jsTreeOptions = {
            "core" : {
                "themes": { "icons": false },
                "check_callback" : true,
                "data": eval(self[0].dataset.id),
                "multiple" : true,
            },
            "plugins" : ["checkbox", "state"],
            "state" : { "key" : jsTreeId },
            "checkbox" : { "three_state" : false, "cascade": "down", "tie_selection" : false },
        };
        const ref = self.jstree(jsTreeOptions);
        const checkedItemsIds = getParameterByName(parameter).split(",");
        self.on("state_ready.jstree", self, function (event, data) {
            const jsTreeRef = self.jstree(true);
            jsTreeRef.check_node(checkedItemsIds);
            const itemsDifferent = jsTreeRef.get_checked().filter(x => checkedItemsIds.indexOf(x) < 0);
            jsTreeRef.uncheck_node(itemsDifferent);
            addJSTreeToolTip();
            highlightParent(jsTreeRef, checkedItemsIds, "#"+jsTreeId);
            self.on("check_node.jstree uncheck_node.jstree", self, function (event, data) {
                reloadTreeSearch(self, parameter);
            });
            self.on("open_node.jstree", self, function (event, data) {
                // On each opening we should recalculate highlighted parents and tooltips
                addJSTreeToolTip();
                highlightParent(jsTreeRef, checkedItemsIds, "#"+jsTreeId);
            })
        });
    });
}
/*
* Initiate the widgets on the articles' overview
*/
publicWidget.registry.sectionsHierarchy = publicWidget.Widget.extend({
    selector: "#knowsystem_left_navigation",
    jsLibs: ["/knowsystem/static/lib/jstree/jstree.min.js"],
    cssLibs: ["/knowsystem/static/lib/jstree/themes/default/style.css"],
    start: function () {
        initiateJsTree("knowsystem_sections", "sections");
        initiateJsTree("knowsystem_tags", "tags");
        initiateJsTree("knowsystem_types", "types");
    },
});
/*
* Likes component
*/
export class ArticleLikesContainer extends Component {
    /*
    * Overwrite to save the initinal state
    */
    setup() {
        this.state = useState({ likes: this.props.likes, dislikes: this.props.dislikes, userState: this.props.userState });
    }
    /*
    * The method to update likes based on the user action
    */
    async _onToggleLike(like) {
        const newState = await rpc.query({
            route: "/knowsystem/like",
            params: { article_int: this.props.articleId, like: like },
        });
        if (newState) { Object.assign(this.state, newState) };
    }
}
ArticleLikesContainer.template = xml`
<a href="#" t-attf-class="btn btn-#{state.userState == 'like' and 'info' or 'primary'}" t-on-click="() => this._onToggleLike(true)">
    <span><span t-out="state.likes"/> <i class="fa fa-thumbs-up ml4"/></span>
</a>
<a href="#" t-attf-class="btn btn-#{state.userState == 'dislike' and 'info' or 'primary'} ml4" t-on-click="() => this._onToggleLike(false)">
    <span><span t-out="state.dislikes"/> <i class="fa fa-thumbs-down ml4"/></span>
</a>`;

/*
* Initiate the like/dislike widget
*/
publicWidget.registry.toggleLikeArticle = publicWidget.Widget.extend({
    selector: ".knowsystem-website-likes",
    /*
    * Re-write to initiate the likes component
    */
    async start() {
        this.component = new ComponentWrapper(this, ArticleLikesContainer, {
            articleId: parseInt(this.el.id),
            likes: parseInt(this.el.dataset.likes),
            dislikes: parseInt(this.el.dataset.dislikes),
            userState: this.el.dataset.ustate,
        })
        this.component.mount(this.el);
    },
});
