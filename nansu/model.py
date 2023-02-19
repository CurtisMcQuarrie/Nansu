from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel, QSqlRelationalTableModel, QSqlRelation
from enum import Enum


class TableType(Enum):
    NonRelational = 0
    Relational = 1


class CustomModel:
    def __init__(self, table_name: str, field_names: list(), table_type: TableType):
        self.table_name = table_name
        self.field_names = field_names
        self.hidden_fields = list()
        self.table_type = table_type
        self.sort_field = field_names[0]
        self.sort_order = Qt.AscendingOrder
        self.model = self._createModel()
        self.sort()

    def _createModel(self):
        """
        create and set up the model
        """
        if self.table_type == TableType.NonRelational.value:
            tableModel = QSqlTableModel()
        else:
            tableModel = QSqlRelationalTableModel()
            
        tableModel.setTable(self.table_name)
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = (field for field in self.field_names)
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)

        return tableModel

    def add(self, data):
        """
        add an instance to the model
        """
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)

        for key, value in data.items():
            if key in self.field_names and key not in self.hidden_fields:
                # get the index for the table
                field_index = self.field_names.index(key)
                self.model.setData(
                    self.model.index(
                        rows,
                        field_index
                    ), value
                )

        self.model.submitAll()
        self.sort()
        self.model.select()

    def delete(self, row):
        """
        delete an instance from the model
        """
        self.model.removeRow(row)
        self.model.submitAll()
        self.sort()
        self.model.select()

    def clear(self):
        """
        clear all instances from the model
        """
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.sort()
        self.model.select()

    def hideFields(self, fields_to_hide: list()):
        self.hidden_fields = fields_to_hide

    def sort(self, sort_field=None, sort_order=None):
        """
        sort the table.
        """
        temp_sort_field = sort_field
        temp_sort_order = sort_order
        if sort_field is None:
            temp_sort_field = self.sort_field
        if sort_order is None:
            temp_sort_order = self.sort_order
        
        if temp_sort_field in self.field_names:
            self.sort_field = temp_sort_field
            self.sort_order = temp_sort_order
            self.model.setSort(self.field_names.index(self.sort_field), self.sort_order)

    def setRelation(field, relation_table, relation_field, displayed_relation_field):
        """
        add a foreign key relation to the model
        """
        if (
            self.table_type == TableType.Relational.value and
            field in self.field_names and 
            relation_field in relation_table.field_names and 
            displayed_relation_field in relation_table.field_names
            ):
            self.model.setRelation(
                self.field_names.index(field),
                QSqlRelation(relation_table.table_name, relation_field, displayed_relation_field)
            )
