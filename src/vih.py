from typing import List,Optional
from dataclasses import dataclass
from graph import Edge,merge_edges

START_BLOCK = "<vih>"
END_BLOCK = "</vih>"
SOURCE_BLOCK = "source"
TARGET_BLOCK = "target"
BLOCK_DELIMINATOR = "|"
STATEMENT_DELIMINATOR = ";"
VALUE_DELIMINATOR = ","

@dataclass
class VIH:
    order:int
    source:List[str]
    target:List[str]

def is_contain_vih(text:str)->bool:
    return START_BLOCK in text and END_BLOCK in text

def get_vih_statement(text:str)->str:

    text = text.strip()

    start = text.index(START_BLOCK) + len(START_BLOCK)

    end = text.index(END_BLOCK)

    return text[start:end].replace(" ","")

def get_vih(vih_statement:str)->Optional[List[VIH]]:
    """
    vih_statement: vih statement must always contains source
    """

    vih:List[VIH] = list()

    statements =  vih_statement.split(STATEMENT_DELIMINATOR)
        
    order = 1 

    for statement in statements:
        if len(statement.replace(" ",""))>1:
            try:
                source = parse_source(statement=statement)
                
                target = parse_target(statement=statement)

                vih.append(
                    VIH
                    (
                        order=order,\
                        source=remove_empty(source),\
                        target=remove_empty(target)
                    )
                )

                order+=1

            except:
                return None
            
    return vih

def parse_source(statement:str)->List[str]:


    start = statement.index(SOURCE_BLOCK)+len(SOURCE_BLOCK)+1

    end  = statement.index(BLOCK_DELIMINATOR)

    return [x.replace(" ","") for x in statement[start:end].split(VALUE_DELIMINATOR)]

def parse_target(statement:str)->List[str]:

    start = statement.index(TARGET_BLOCK)+len(TARGET_BLOCK)+1

    end  = statement.index(BLOCK_DELIMINATOR,statement.index(BLOCK_DELIMINATOR)+1)

    return [x.replace(" ","") for x in statement[start:end].split(VALUE_DELIMINATOR)]

def remove_empty(values:List[str])->List[str]:
    return [x for x in values if len(x)>0]

def vih_to_edge(vih:VIH)->List[Edge]:
    edges:List[Edge] = list()

    for source in vih.source:
        edges.append(
            Edge
            (
                node_name=source,
                parent_nodes=[]
            )
        )

    for target in vih.target:
        edges.append(
            Edge
            (
                node_name=target,
                parent_nodes=vih.source
            )
        )
    
    return edges

def vihs_to_edges(vihs:List[VIH])->List[Edge]:
    
    graphs:List[List[Edge]] = list()

    for vih in vihs:
        graphs.append(vih_to_edge(vih=vih))

    return merge_edges(graphs=graphs)