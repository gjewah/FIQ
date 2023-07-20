/** @odoo-module */

import { TaskChecklist } from "@task_checklist/components/task_checklist/task_checklist";
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useService } from "@web/core/utils/hooks";
import { useX2ManyCrud } from "@web/views/fields/relational_utils";


export class TaskChecklistField extends Component {
    /*
    * Overwrite to add own actions and services
    */
    setup() {
        const { saveRecord, removeRecord } = useX2ManyCrud( () => this.list, true);
        this.saveRecord = saveRecord;
        this.removeRecord = removeRecord;
    }
    /*
    * The method to prepare props for the component TaskChecklist
    */
    checkListProps() {
        return {
            checkPoints: this.list.records.map((record) => record.data.id),
            stageId: this._convertFormData(this.props.record.data.stage_id),
            onToggleApprove: this.onToggleApprove.bind(this),
            readonly: this.props.readonly,
        }
    }
    /*
    * Getter for the list
    */
    get list() {
        return this.props.value;
    }
    /*
    * The method to add/remove new record
    */
    async onToggleApprove(checkPointId, alreadyApproved) {
        if (alreadyApproved) {
            const record = this.getRecordById(checkPointId);
            if (record) { await this.removeRecord(record) };
        }
        else { await this.saveRecord([checkPointId]) }
    }
    /*
    * The method to find a record by id
    */
    getRecordById(recordId) {
        const recordList = this.list.records.filter(rec => rec.data.id == recordId);
        if (recordList.length != 0) { return recordList[0] }
        return false
    }
    /*
    * The method to convert form data to real ids
    */
    _convertFormData(fieldValue) {
        return fieldValue && fieldValue.length != 0 ? fieldValue[0] : false
    }
}

TaskChecklistField.template = "task_checklist.TaskChecklistField";
TaskChecklistField.components = { TaskChecklist };
TaskChecklistField.props = { ...standardFieldProps };
TaskChecklistField.supportedTypes = ["many2many"];
TaskChecklistField.isSet = (value) => value.count > 0;

registry.category("fields").add("task_checklist", TaskChecklistField);
