#Adding personalised RDA values from sample user
from . import db
from .models import RDAValues, UserPersonalRDA

def addPersonalisedRDATest():
    profile_rda_values = db.session.query(RDAValues).filter_by(rda_profile_id=current_user.rda_profile_id).all()

    for row in profile_rda_values:
        if '_per_kg' in row.unit:
            weight_adjusted_value = row.value * current_user.weight_kg
        else:
            weight_adjusted_value = row.value
        exists = db.session.query(UserPersonalRDA).filter_by(user_id=current_user.id, nutrient=row.nutrient_name).first() is not None
        if not exists:
            personal_rda = UserPersonalRDA(
                user_id = current_user.id,
                nutrient=row.nutrient_name,
                rda = weight_adjusted_value
            )
            db.session.add(personal_rda)
        else:
            if db.session.query(UserPersonalRDA).filter_by(user_id=current_user.id, nutrient=row.nutrient_name).first().rda == weight_adjusted_value:
                continue
            else:
                db.session.query(UserPersonalRDA).filter_by(user_id=current_user.id, nutrient=row.nutrient_name).first().rda = weight_adjusted_value
    db.session.commit()