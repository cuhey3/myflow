import asyncio
from producer import *
from endpoints import Endpoints
from exchange import Exchange
from components import *
from expression import *


def foo(string):
    async def process(exchange):
        assert (isinstance(exchange.get_body(), str))
        exchange.set_body(exchange.get_body() + ' ' + string)
        return exchange

    return process


async def ppp(exchange):
    print(exchange.get_body())


def predicate(exchange):
    return True

(RouteId('myroute').to(foo('bar')).to(foo('wao')).when([
        (predicate, To(foo('poko')).to(foo('pai'))),
        (False, To(foo('pen')).to(foo('pee')).when([
            (False, To(foo('nyao'))),
            (False, To(foo('passo')))]))
        ])
    .to(foo('final'))
    .to(log({}))
    .filter(True)
    .to(foo('papaiya'))
    #.split(body, To(ppp))
) #yapf:disable

RouteId('myfoo').to(cache({
    'to': 'myroute',
    'keys': [header('pon.puu')]
})).to(direct({
    'to': 'myroute'
})).split(body(), To(ppp))


def gather_func(exchanges):
    gathered_body = exchanges[0].get_body() + " " + exchanges[1].get_body()
    exchanges[0].set_body(gathered_body)
    return exchanges[0]


RouteId('gather_a').to(foo('bon'))
RouteId('gathering').gather([To(direct({
    'to': 'gather_a'
})), To(foo('poyo'))], gather_func)

Timer({'repeatCount': 3}).to(log({}))


async def tasks_main():
    #yapf:disable
    exchange = await Endpoints().send_to('myfoo',Exchange("poko",{'foo': 'bar','pon': {'puu': 'poo'}}))
    exchange = await Endpoints().send_to('myfoo',Exchange("poko",{'foo': 'bar','pon': {'puu': 'poo'}}))
    gathering_exchange = await Endpoints().send_to('gathering', Exchange('boo'))
    #yapf:enable
    if exchange:
        print(exchange.get_body())
    if gathering_exchange:
        #expect: boo bon boo poyo
        print('gathered:', gathering_exchange.get_body())


asyncio.get_event_loop().run_until_complete(tasks_main())
asyncio.get_event_loop().run_forever()
'''
#yapf:disable
exchange = Endpoints().send_to('myfoo',Exchange("poko",{'foo': 'bar','pon': {'puu': 'poo'}}))
exchange = Endpoints().send_to('myfoo',Exchange("poko",{'foo': 'bar','pon': {'puu': 'poo'}}))
#yapf:enable
if exchange:
    print(exchange.get_body())
'''
