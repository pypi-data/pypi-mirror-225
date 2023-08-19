from sqlalchemy import select, insert, or_, String, cast


class FilterMeta(type):
    """
    Delete required fields from the common pool of variables
    Add meta variable for further query building
    *Add validate options
    """

    def __new__(cls, name, bases, dct):
        if bases:
            attrs = {}
            for name, value in dct.items():
                if isinstance(value, Query):
                    attrs[name] = value.options

            dct['meta'] = attrs
            ann = dct.get('__annotations__')
            new_ann = {}
            for name, value in attrs.items():
                if value.get('required', False):
                    del dct[name]
                    new_ann[name] = ann[name]
                else:
                    dct[name] = None
            new_ann.update(ann)
            dct['__annotations__'] = new_ann
        return type.__new__(cls, name, bases, dct)


class Query:
    """
    option = like, ilike, in, !=, == and returned_fields
    required = True/False
    json = True/False This field is json?
    parent = name of json field id json=True
    alias = don't touch
    """

    def __init__(self, **options):
        self.options = options


class Filter(metaclass=FilterMeta):
    def __new__(cls, *args, **kwargs):
        # for name, value
        return FilterBase(meta=cls.meta, fields=kwargs)


class FilterBase:

    def __init__(self, meta, fields=None):
        self.meta = meta
        self.data_fields = {}
        for name, value in fields.items():
            if value != 'None':
                if self.meta.get(name):
                    self.meta[name].update({'value': value})
                self.data_fields[name] = value
            else:
                self.meta[name].update({'value': None})

            # setattr(self, name, value)
        # self.data_fields = type('Data', (), self.data_fields)

    def filter(self, query):
        #### if alchemy .....
        return self.__alchemy_filter(query=query)

    def __alchemy_filter(self, query):
        """ Вытащить класс модели и начать манипуляции с операторами
        возвращает объект запроса sqlalchemy
        """
        # like, ilike, in, ==, returned_fileds, !!json_fields!!
        # Проверять есть ли возвращаемое поле у Модели
        returned = []
        params = []
        models, operator = self.__get_alchemy_models(query)
        for param, options in self.meta.items():
            option = options.get('option')
            value = options.get('value')
            json_column = options.get('json_column')
            if value is None:
                continue
            if option == 'returned_fields':
                if returned:
                    continue
                returned = self.__returned_fields(models=models, value=value)
                continue
            if json_column:
                field = self.__get_json_field(models=models, child=param, parent=json_column)
            else:
                field = self.__get_field(models=models, param=param)
            params = params + self.__create_exp(param=field, values=value, option=option)
        if not returned:
            return query.filter(or_(*params))
        return operator(*returned).filter(or_(*params))

    def __get_alchemy_models(self, query):
        models = {}
        operator = None
        for column in query.column_descriptions:
            models[column.get('name')] = {
                'fields': [name for name, value in column.get('entity').__dict__.items() if
                           not name.startswith('__') and name != '_sa_class_manager'],
                'model': column.get('type'),
            }
        if query.is_select:
            operator = select
        elif query.is_dml:
            operator = insert
        return models, operator

    def __returned_fields(self, models, value):
        returned_fields = []
        fields = value.replace(' ', '').split(',')
        for field in fields:
            field, child = field.split('.') if '.' in field else (field, None)
            for name, values in models.items():
                if field in values.get('fields'):
                    attr = getattr(values.get('model'), field)
                    returned_fields.append(attr[child].label(child) if child else attr)  # add as
        return returned_fields

    def __get_json_field(self, models, child, parent):
        for name, values in models.items():
            if parent in values.get('fields'):
                attr = getattr(values.get('model'), parent)[child]  # casts types
                return cast(attr, String)

    def __get_field(self, models, param):
        for name, values in models.items():
            if param in values.get('fields'):
                attr = getattr(values.get('model'), param)
                return attr

    def __create_exp(self, param, values, option):
        if not values:
            return
        values = values.replace(' ', '').split(',')
        if option == 'like':
            return [param.like('{}'.format(value)) for value in values]
        elif option == 'ilike':
            return [param.ilike('%{}%'.format(value)) for value in values if value]
        elif option == 'in':
            return [param.in_(values)]
        elif option == '==':
            return [param == value for value in values]
        elif option == '!=':
            return [param != value for value in values]
