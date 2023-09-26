/** @odoo-module **/

import { _lt } from "@web/core/l10n/translation";
import { FormViewDialog } from "@web/views/view_dialogs/form_view_dialog";
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart, useState } = owl;

const componentModel = "knowsystem.tour";


export class KnowSystemLearningTours extends Component {
    /*
    * Re-write to import required services and update props on the component start
    */
    setup() {
        this.state = useState({ toursData: null });
        this.orm = useService("orm");
        this.actionService = useService("action");
        this.dialogService = useService("dialog");
        onWillStart(async () => {
            await this._loadLearningTours(this.props);
        });
    }
    /*
    * The method to load available tours
    */
    async _loadLearningTours(props) {
        const toursData = await this.orm.call(componentModel, "action_return_tours", []);
        Object.assign(this.state, { toursData: toursData });
    }
    /*
    * The method to launch the learning tour
    */
    async _onTourStart(tourId) {
        const actionDict = await this.orm.call(componentModel, "action_return_start_page", [tourId])
        await this.actionService.doAction(actionDict);
    }
    /*
    * The method to add the very root tour
    */
    async _onOpenTour(tourId) {
        const modelContext = this.props.kanbanModel.rootParams.context;
        this.dialogService.add(FormViewDialog, {
            resModel: componentModel,
            resId: tourId,
            context: modelContext,
            title: _lt("Learning Tour"),
            preventCreate: this.props.canCreate ? false : true,
            preventEdit: this.props.canCreate ? false : true,
            onRecordSaved: async (formRecord) => { 
                await this._loadLearningTours(this.props);
            },
        }); 
    }
    /*
    * The method to open the tour for edition
    */
    async _onEditTour(tourId) {
        if (this.props.canCreate) { this._onOpenTour(tourId) };
    }
}

KnowSystemLearningTours.template = "knowsystem.KnowSystemLearningTours";
