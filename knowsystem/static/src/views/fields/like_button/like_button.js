/** @odoo-module **/

import { IntegerField } from "@web/views/fields/integer/integer_field";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";


export class LikeButtonField extends IntegerField {
    /*
    * Re-write to add own services and actions
    */
    setup() {
        this.orm = useService("orm");
        super.setup(...arguments);
    }
    /*
    * Getter for thisLikeState
    */
    get thisLikeState() {
        return this.props.record.data.this_user_like_state;
    }
    /*
    * The method to save like/dislike
    */
    async toggleLike() {
        if (this.props.record.data.id) {
            const newLikesList = await this.orm.call(
                "knowsystem.article",
                this.props.action,
                [[this.props.record.data.id]],
            );
            const changes = {
                "likes_number": newLikesList[0],
                "dislikes_number": newLikesList[1],
                "this_user_like_state": newLikesList[2],
            }
            this.props.record.update(changes);
            this.props.record.save();
        }
    }
};

LikeButtonField.supportedTypes = ["integer"];
LikeButtonField.template = "knowsystem.LikeButtonField";
LikeButtonField.props = {
    ...IntegerField.props,
    icon: { type: String, optional: false },
    action: { type: String, optional: false },
    likeState: { type: String, optional: false },
};
LikeButtonField.extractProps = ({ attrs, field }) => {
    var charExtraProps = IntegerField.extractProps({ attrs, field })
    return Object.assign( 
        charExtraProps, 
        { 
            icon: attrs.icon,
            action: attrs.action,
            likeState: attrs.like_state,
        },
    );
}

registry.category("fields").add("likeButtonField", LikeButtonField);
