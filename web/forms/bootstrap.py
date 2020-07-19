# _author: 17393
# date: 2020/5/17


class BootstrapForm(object):

    bootstrap_class_exclude = []

    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.bootstrap_class_exclude:
                continue
            old_class = field.widget.attrs.get('class', "")
            field.widget.attrs['class'] = '{} form-control'.format(old_class)
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)
