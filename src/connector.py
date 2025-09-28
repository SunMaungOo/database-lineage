from typing import List,Optional
from database import query
from graph import Edge,merge_edges
from config import GET_VIEW_LINEAGE,GET_PROCEDURE_LINEAGE
from vih import get_vih,get_vih_statement,is_contain_vih,VIH,vihs_to_edges



def get_view_lineage(connection_str:str,\
                    host:str,\
                    database:str,\
                    is_fqn:bool=True)->Optional[List[Edge]]:

    try:

        graphs:List[Edge] = list()

        for row in query(connection_str=connection_str,\
                         query=GET_VIEW_LINEAGE):
            
            view_schema = row[0]

            view_name = row[1]

            used_schema_name = row[2]

            used_table_name = row[3]

            target = get_name(
                host=host,\
                database=database,\
                name=f"{view_schema}.{view_name}",\
                is_fqn=is_fqn
            )

            source = get_name(
                host=host,\
                database=database,\
                name=f"{used_schema_name}.{used_table_name}",\
                is_fqn=is_fqn
            )

            graphs.append(Edge(
                node_name=target,\
                parent_nodes=[source]
            ))

        return merge_edges(graphs=graphs)
        
    except:
        return None
    

def get_procedure_lineage(connection_str:str,\
                    host:str,\
                    database:str,\
                    is_fqn:bool=True)->Optional[List[Edge]]:
    
    try:

        vihs:List[VIH] = list()

        for row in query(connection_str=connection_str,\
                         query=GET_PROCEDURE_LINEAGE):
            
            routine_definition = row[2]

            if not is_contain_vih(text=routine_definition):
                continue

            vih_statement = get_vih_statement(text=routine_definition)

            vih = get_vih(vih_statement=vih_statement)

            if vih is None:
                continue

            vihs.append(vih)

        vihs = clean_vihs(vihs=vihs)

        if is_fqn:
            vihs = add_fqn(vihs=vihs,\
                           host=host,\
                           database=database)

        return vihs_to_edges(vihs=vihs)
    
    except:
        return None


def get_name(host:str,\
            database:str,\
            name:str,\
            is_fqn:bool=True):
    
    if is_fqn:

        blocks = name.split(".")

        block_lengths = len(blocks)

        # get only the schema name and table name

        if block_lengths>2:
            name = blocks[block_lengths-2]+"."+blocks[block_lengths-1] 

        name = f"{host}.{database}.{name}"


    return name

def clean_vihs(vihs:List[VIH])->List[VIH]:

    return [VIH(
        order=vih.order,\
        source=list(set(vih.source)),\
        target=list(set(vih.target))
    ) for vih in vihs]

def add_fqn(vihs:List[VIH],\
            host:str,\
            database:str)->List[VIH]:
    
    fqn_vihs:List[VIH] = list()
    
    for vih in vihs:

        source = [get_name(host=host,\
                         database=database,
                         name=x,\
                        is_fqn=True) for x in vih.source]
        
        target = [get_name(host=host,\
                         database=database,
                         name=x,\
                        is_fqn=True) for x in vih.target]
        
        fqn_vihs.append(VIH(
            order=vih.order,
            source=source,\
            target=target
        ))
        

    return fqn_vihs

    




