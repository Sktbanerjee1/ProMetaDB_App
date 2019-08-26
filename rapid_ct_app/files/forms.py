from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class UpdateFileForm(FlaskForm):
    sample_type = SelectField(
        validators=[DataRequired()],
        choices=[
            ('Bleed(ICH)', 'Bleed - Intracranial Hemorrhage '),
            ('Control(Normal)', 'Normal -  No Intracranial Hemorrhage '),
            ('Lesion', 'Lesion -  No Intracranial Hemorrhage '),
            ('Calcification', 'Calcification -  No Intracranial Hemorrhage ')
        ]
        )
    submit = SubmitField('Update Annotation')