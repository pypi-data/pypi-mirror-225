from .executer import ExecuterCaller
from .common import intersect

class Prework:

    def __init__(self,
                 caller: ExecuterCaller, 
                 preworks: list,
                 agent_roles: list) -> None:

        self.caller = caller
        
        for prework in preworks:

            if prework.get('agent_roles') \
                and not intersect(agent_roles, prework.get('agent_roles')):
                continue
            if not prework.get('executer'):
                continue

            self._do_prework(prework)

    def _do_prework(self, prework: dict):
        
        from . import app, zipkin
        with app.app_context():

            if zipkin:

                zipkin.create_span('prework')
                zipkin.update_tags(param=prework)

            rtn, results = self.caller.execute_command(prework)

            if zipkin:
                zipkin.update_tags(
                    param  = prework,
                    result = results,
                )

