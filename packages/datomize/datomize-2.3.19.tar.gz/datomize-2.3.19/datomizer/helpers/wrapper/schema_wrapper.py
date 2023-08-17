from typing import Optional
from datomizer.protos.autodiscoveryservice_pb2 import SchemaDiscoveryDTO, TableDTO, ColumnDTO, DependencyDTO, TableRefDTO, Key, UserActionsKeys
from datomizer.utils.exceptions import TableNotFound, ColumnNotFound
from datomizer.utils.messages import TABLE_NOT_EXISTS, COLUMN_NOT_EXISTS


class SchemaWrapper(object):
    schema: SchemaDiscoveryDTO

    def __init__(self, schema):
        self.schema = schema

    def tables(self) -> list:
        return self.schema.tables

    def tables_name(self) -> list:
        return map(lambda table: table.name, self.tables())

    def table(self, table_name=None) -> TableDTO:
        if not table_name and len(self.tables()) == 1:
            return self.tables()[0]

        tables = self.tables()
        table: TableDTO
        for table in tables:
            if table_name == table.name:
                return table

        raise TableNotFound(TABLE_NOT_EXISTS)

    def columns(self, table_name=None) -> list:
        return self.table(table_name).columns

    def column(self, table_name, column_name) -> ColumnDTO:
        columns = self.columns(table_name)
        column: ColumnDTO
        for column in columns:
            if column_name == column.name:
                return column

        raise ColumnNotFound(COLUMN_NOT_EXISTS)

    def add_foreign_key(self, table_name: str, column_name: str, key_id: Optional[int] = None) -> Key:
        tbl = self.table(table_name)
        col = self.column(table_name, column_name)  # doubles as check for column existence
        fk_ids = [0] + [key.id for key in tbl.foreignKeys]
        if key_id is not None:
            assert key_id not in fk_ids, f'key_id {key_id} already exists'
        else:
            key_id = max(fk_ids) + 1

        fk = Key(keyId=key_id, columnName=[col.name])
        tbl.foreignKeys.append(fk)
        return fk

    def add_relation_one2many(self, table_one: str, column_one: str, table_many: str, column_many: str) -> DependencyDTO:
        """Adds one-to-many relation between two tables.
        Args:
            table_one (str): name of the table with the primary key
            column_one (str): name of the primary key column
            table_many (str): name of the table with the foreign key
            column_many (str): name of the foreign key column
        Returns:
            DependencyDTO added relation
        """
        tbl_l: TableDTO = self.table(table_one)
        col_l = self.column(table_one, column_one)
        col_l.role = 'identifier_code'
        col_l.isIgnore = False
        col_l.isSupported = True
        self.__set_map_value(col_l.userActions, UserActionsKeys, UserActionsKeys.IS_IGNORE, False)
        assert len(tbl_l.primaryKey.columnName) == 0 or column_one in tbl_l.primaryKey.columnName, 'Another primary key already exists in table_one'
        if len(tbl_l.primaryKey.columnName) == 0:
            tbl_l.primaryKey.columnName.append(column_one)

        tbl_r: TableDTO = self.table(table_many)
        col_r = self.column(table_many, column_many)
        self.__set_map_value(col_r.userActions, UserActionsKeys, UserActionsKeys.IS_IGNORE, False)
        col_r.role = 'identifier_code'
        col_r.isIgnore = False
        col_r.isSupported = True
        fk_tbl_r = [fk for fk in tbl_r.foreignKeys if column_many in fk.columnName]
        if len(fk_tbl_r) == 0:
            fk_tbl_r = [self.add_foreign_key(table_many, column_many)]

        dep = DependencyDTO(
            left=TableRefDTO(tableName=table_one,
                             keyId=0, keyType=TableRefDTO.KeyType.PK,
                             cardinalityType=TableRefDTO.CardinalityType.One,
                             relationshipType=TableRefDTO.RelationshipType.Contains),
            right=TableRefDTO(tableName=table_many,
                              keyId=fk_tbl_r[0].keyId, keyType=TableRefDTO.KeyType.FK,
                              cardinalityType=TableRefDTO.CardinalityType.Many,
                              relationshipType=TableRefDTO.RelationshipType.Contained)
        )
        self.schema.dependencies.append(dep)
        return dep

    @staticmethod
    def __set_map_value(map_dict, enum, key_index, value):
        map_dict[enum.Name(key_index)] = value

    def __str__(self):
        return str(self.schema)
