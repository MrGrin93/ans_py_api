from fastapi import FastAPI, Body 
from pydantic import BaseModel, IPvAnyAddress, IPvAnyNetwork 
from typing import List, Union, Tuple 
import yaml 
 
class Host(BaseModel): 
    host: Union[IPvAnyAddress, IPvAnyNetwork] 
    port_protocol: Union[int, Tuple[int, int], None] = None 
 
class ACLine(BaseModel): 
    source: Host 
    destination: Host 
    protocol: str 
 
class ACL(BaseModel): 
    name: str 
    aces: List[ACLine] 
 
 
app = FastAPI() 
 
@app.post('/') 
async def create_pb(acl: ACL = Body( 
        examples={ 
            "normal":{ 
                "summary": "A normal example", 
                "description": "A normal item works correctly.", 
                "value": { 
                        "name": "string", 
                        "aces": [ 
                        { 
                        "source": { 
                            "host": "172.24.0.0/24", 
                            "port_protocol": 80 
                        }, 
                        "destination": { 
                            "host": "172.24.1.2", 
                            "port_protocol": [8080, 8090] 
                        }, 
                        "protocol": "tcp" 
                        }, 
                        { 
                        "source": { 
                            "host": "172.24.1.0/24" 
                        }, 
                        "destination": { 
                            "host": "172.24.3.2", 
                            "port_protocol": [8080, 8090] 
                        }, 
                        "protocol": "tcp" 
                        } 
                        ] 
                    } 
                } 
            } 
            )): 
 
    
 
    return acl
