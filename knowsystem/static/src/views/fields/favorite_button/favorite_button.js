/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
const { Component } = owl;

export class FavoriteButtonField extends Component {
    /*
    * Re-write to add own services and actions
    */
    setup() {
        this.orm = useService("orm");
        super.setup(...arguments);
    }
    /*
    * The method to toggle favorite
    */
    async toggleFavorite() {
        if (this.props.record.data.id) {
            const thisUserFavorite = await this.orm.call(
                "knowsystem.article",
                "action_toggle_favorite",
                [[this.props.record.data.id]],
            );
            this.props.record.update({ "this_user_favorite": thisUserFavorite });
            this.props.record.save();
        }
    }
};

FavoriteButtonField.supportedTypes = ["boolean"];
FavoriteButtonField.template = "knowsystem.FavoriteButtonField";


registry.category("fields").add("favoriteButtonField", FavoriteButtonField);
