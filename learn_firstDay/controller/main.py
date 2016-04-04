# -*- coding: utf-8 -*-
from json import JSONEncoder

from openerp import api, http, tools
from openerp.http import request


class zndx(http.Controller):
    @http.route('/hello/<int:a>/<string:b>', type='http', auth='public', method=['post', 'get'], website=True)
    def index(self, *args, **kwargs):
        # return "hello,world"

        res = request.env['zndx.restaurant'].search([('name', '=', '铁道学院食堂')])

        if 'a' in kwargs:
            print 'a:%s b:%s' % (kwargs['a'], kwargs['b'])

        return http.request.render('learn_firstDay.index', {'restaurant': res})

    @http.route('/hello1/<string:a>/', type='http', auth='public', method=['post', 'get'])
    def index1(self, a, *args, **kwargs):
        return "hello,%s" % a

    @http.route('/hello2', type='http', auth='public', method=['post', 'get'])
    def index2(self, *args, **kwargs):
        return "hello,world"

    @http.route('/order', type='http', auth='public', method=['post', 'get'], csrf=False, website=True)
    def index3(self):
        res = request.env['zndx.restaurant'].search([('name', '=', '铁道学院食堂')])
        return http.request.render('learn_firstDay.order_form', {'restaurant': res})

    @http.route('/websites/restaurant/order', type='http', auth='public', website=True, csrf=False)
    def show_order(self):
        res = request.env['zndx.restaurant'].sudo().search([], limit=1)
        return http.request.render('learn_firstDay.order', {'restaurant': res})

    @http.route('/add_soup/<string:soupname>/<float:price>', type='http', auth='public', method=['post', 'get'])
    def index1(self, soupname, price, *args, **kwargs):
        res = request.env['zndx.restaurant'].sudo().search([], limit=1)
        soup_vals = {'name': soupname, 'price': float(price), 'restaurant_id': res.id}
        res.write({'soup_ids': [(1, 3, soup_vals)]})
        return "add soup is ok."

    @http.route('/add_waiter/<int:type>/<int:waiter_id>', type='http', auth='public', method=['post', 'get'])
    def index1(self, type, waiter_id, *args, **kwargs):
        res = request.env['zndx.restaurant'].sudo().search([], limit=1)
        res.write({'waiter_ids': [(type, waiter_id, [1, 2])]})
        return "process waiter is ok."

    @http.route('/get_soup/<int:soup_id>', type='http', auth='public', method=['post', 'get'])
    def get_soup(self, soup_id, *args, **kwargs):
        soup = request.env['zndx.soup'].sudo().browse(soup_id)
        retstr = {'id': soup.ids[0], 'name': soup.name, 'price': soup.price}
        return JSONEncoder().encode(retstr)

    @http.route('/submit_form/', type='http', auth='public', method=['post', 'get'], website=True, csrf=False)
    def index6(self, *args, **kwargs):
        # attachment_id = request.env['zndx.order'].sudo().create()
        # name= kwargs['soup_id'].split('-')[0]

        print kwargs
        price = kwargs['soup_id'].split(' ')[1]

        value = {'soup_id': int(kwargs['soup_id']),
                 'restaurant_id': int(kwargs['restaurant_id']),
                 'partner_id': int(kwargs['partner_id']),
                 'price': float(price)
                 }
        print value
        request.env['zndx.order'].sudo().create(value)

        return "122"
