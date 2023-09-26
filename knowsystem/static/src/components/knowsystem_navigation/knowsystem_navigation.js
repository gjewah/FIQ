/** @odoo-module **/

import { loadCSS, loadJS } from "@web/core/assets";
import { Domain } from "@web/core/domain";
import { _lt } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { KnowSystemJsTreeContainer } from "@knowsystem/components/knowsystem_jstree_container/knowsystem_jstree_container";
import { KnowSystemLearningTours } from "@knowsystem/components/knowsystem_learning_tours/knowsystem_learning_tours";
const { Component, onWillStart } = owl;

const componentModel = "knowsystem.article";
const searchSections = { "sections": _lt("Sections"), "tags": _lt("Tags"), "types": _lt("Types") }


export class KnowSystemNavigation extends Component {
    /*
    * Re-write to import required services and update props on the component start
    */
    setup() {
        this.orm = useService("orm");
        this.kanbanOrder = "views_number_internal"; // this is default order
        this.asc = true;
        this.jsTreeDomain = [];
        this.jsTreeDomains = {};
        onWillStart(async () => {
            const proms = [
                loadJS("/knowsystem/static/lib/jstree/jstree.min.js"),
                loadCSS("/knowsystem/static/lib/jstree/themes/default/style.css"),
            ]
            return Promise.all(proms);
        });
    }
    /*
    * The method to prepare jstreecontainer props
    */
    getJsTreeProps(key) {
        return {
            jstreeTitle: searchSections[key],
            jstreeId: key,
            kanbanModel: this.props.kanbanList.model,
            onUpdateSearch: this.onUpdateSearch.bind(this),
            canCreate: key != "types" ? this.props.canCreate : this.props.canDelete,
        }
    }
    /*
    * The method to prepare tours' props
    */
    getToursProps() {
        return {
            kanbanModel: this.props.kanbanList.model,
            canCreate: this.props.canDelete,
        }
    }
    /*
    * The method to prepare the domain by all JScontainers and notify searchmodel
    */
    onUpdateSearch(jstreeId, domain) {
        var jsTreeDomain = this._prepareJsTreeDomain(jstreeId, domain);
        if (this.jsTreeDomain != jsTreeDomain) {
            this.jsTreeDomain = jsTreeDomain;
            this.env.searchModel.toggleJSTreeDomain(this.jsTreeDomain, {name: this.kanbanOrder, asc: !this.asc});
        };
    }
    /*
    * The method to prepare domain based on all jstree components
    */
    _prepareJsTreeDomain(jstreeId, domain) {
        var jsTreeDomain = [];
        this.jsTreeDomains[jstreeId] = domain;  
        _.each(this.jsTreeDomains, function (val_domain) {
            jsTreeDomain = Domain.and([jsTreeDomain, val_domain])
        });
        return jsTreeDomain
    }
    /*
    * The method to select all records that satisfy search criteria
    * It requires orm.call since not all records are shown on the view
    */
    async _onSelectAll() {
        const kanbanModel = this.props.kanbanList.model;
        var fullDomain = this.env.searchModel._getDomain();
        if (fullDomain.length != 0) {
            const selectedRecords = kanbanModel.selectedRecords.map((rec) => rec.id);
            fullDomain = Domain.or([fullDomain, [["id", "in", selectedRecords]]]).toList();            
        };
        kanbanModel.selectedRecords = await this.orm.searchRead(componentModel, fullDomain, ["name"]);
        await kanbanModel.root.load();
        kanbanModel.notify();        
    }
    /*
    * The method to reseqeunce kanban list
    * We clear orderBy each time since the UI assumes sorting only by a single criteria
    */
    async _applySorting() {
        this.props.kanbanList.orderBy = [];
        this.props.kanbanList.orderBy.push({name: this.kanbanOrder, asc: this.asc});
        this.props.kanbanList.orderBy.push({name: "id"});
        this.env.searchModel.updateOrderBy({name: this.kanbanOrder, asc: !this.asc});
        await this.props.kanbanList.sortBy(this.kanbanOrder);
    }

    /*
    * The method to sort records by specific field (always in desc order)
    */
    async _onApplySorting(event) {
        this.kanbanOrder = event.currentTarget.value;
        this.asc = this.kanbanOrder == "views_number_internal" || this.kanbanOrder == "likes_score" ? true : false;
        await this._applySorting();
    }
    /*
    * The method to sort records by previously chosen field in the reverse (to the previously adapted) order
    */
    async _onApplyReverseSorting() {
        this.asc = !this.asc;
        await this._applySorting();
    }
};

KnowSystemNavigation.template = "knowsystem.KnowSystemNavigation";
KnowSystemNavigation.components = { KnowSystemJsTreeContainer, KnowSystemLearningTours }
