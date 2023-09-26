/** @odoo-module */

import { formatDateTime, parseDateTime } from "@web/core/l10n/dates";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useService } from "@web/core/utils/hooks"
const { Component, onWillStart, onWillUpdateProps, useState } = owl;


export class RevisionsTable extends Component {
    /*
    * Overwrite to introduce our own services
    */
    setup() {
        this.orm = useService("orm");
        this.state = useState({ revisionsList: null });
        this.actionService = useService("action");
        onWillStart(async () => {
            await this._loadRevisions(this.props);
        });
        onWillUpdateProps(async (nextProps) => {
            await this._loadRevisions(nextProps);
        })
    }
    /*
    * The method to preprocess record data before showing 
    */
    _preprocessRevisions(revisionsList) {
        return revisionsList.map(m => ({
            ...m,
            published_date_str: 
                formatDateTime(
                    parseDateTime(
                        m.change_datetime,
                        { format: 'MM-dd-yyy HH:mm:ss' },
                    ),
                )
        }));
    }
    /*
    * The method to load revisions data
    */
    async _loadRevisions(props) {
        const recordIds = props.value.records.map((record) => record.resId);
        const revisionsList = await this.orm.call(
            "knowsystem.article.revision",
            "action_get_revisions",
            [recordIds],
        );
        Object.assign(this.state, { revisionsList: this._preprocessRevisions(revisionsList) });
    }
    /*
    * The method to execute action of showing the revision
    */
    async onObserve(revisionId) {
        await this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: "knowsystem.article.revision",
            res_id: revisionId,
            views: [[false, "form"]],
        });
    }
}

RevisionsTable.template = "knowsystem.RevisionsTable";
RevisionsTable.props = {...standardFieldProps};
RevisionsTable.supportedTypes = ["one2many"];
RevisionsTable.isSet = (value) => value.count > 0;

registry.category("fields").add("revisionsTable", RevisionsTable);
