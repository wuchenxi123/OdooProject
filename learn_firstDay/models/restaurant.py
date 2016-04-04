# -*- coding: utf-8 -*-

import datetime
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models, _


class Restaurant(models.Model):
    _name = "zndx.restaurant"
    _description = u"饭店"

    name = fields.Char(string=u'饭店名称', required=True, default=u'铁道学院食堂', index=True, size=20)
    soup_ids = fields.One2many('zndx.soup', 'restaurant_id', string=u"销售的汤")
    waiter_ids = fields.Many2many('zndx.waiter', 'zndx_restaurant_waiter_rel', 'restaurant_id', 'waiter_id',
                                  string=u'服务员')

    type = fields.Selection([
        (u'自营', u'自营'),
        (u'加盟', u'加盟'),
    ], required=True, default=u'自营',
        string=u'经营类型')
    note = fields.Text(string=u'备注')


class Soup(models.Model):
    _name = "zndx.soup"
    _description = u"汤"

    name = fields.Char(string=u'名称', required=True, index=True, size=20)
    restaurant_id = fields.Many2one('zndx.restaurant', string=u"饭店", help=u"请选择一个饭店")
    price = fields.Float(u'价格', default=1.0, required=True)


class Waiter(models.Model):
    _name = 'zndx.waiter'
    _description = u'服务员'

    name = fields.Char(u'服务员', required=True)


class Order(models.Model):
    _name = 'zndx.order'
    _description = u'订单'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char(u'订单编号', default="/", index=True, readonly=True)
    partner_id = fields.Many2one('res.partner', u'顾客')
    restaurant_id = fields.Many2one('zndx.restaurant', u'饭店')
    soup_id = fields.Many2one('zndx.soup', string=u'汤', domain="[('restaurant_id','=',restaurant_id)]")
    price = fields.Float(u'价格', default=0.0)
    payment = fields.Float(u'实付金额', default=0.0)
    state = fields.Selection([(u'未付款', u'未付款'), (u'已付款', u'已付款'), (u'已上菜', u'已上菜'), (u'已完成', u'已完成'), ], u'状态',
                             default=u'未付款')
    tax = fields.Float(u'税', compute='_compute_tax', store=True)

    @api.multi
    @api.depends('price')
    def _compute_tax(self):
        for order in self:
            order.tax = order.price * 0.17

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].get(
                'zndx.order') or '/'
        return super(Order, self).create(vals)

    @api.multi
    @api.onchange('soup_id')
    def set_price(self):
        for order in self:
            order.price = order.soup_id.price

    @api.multi
    @api.constrains('price')
    def _check_price(self):
        for order in self:
            if order.price <= 0:
                raise ValidationError(u'价格不能为负数或0')

    @api.multi
    def pay1(self):
        self.write({'state': u'已上菜'})

    @api.multi
    def pay2(self):
        self.write({'state': u'已完成'})


class OrderPayWizard(models.TransientModel):
    _name = "zndx.order_pay_wizard"

    def set_order_id(self):
        print self._context.get('active_id')
        orders = self.env['zndx.order'].search([('id', '=', self._context.get('order_id'))])
        if orders and len(orders):
            return orders[0]

    order_id = fields.Many2one('zndx.order', u'订单', readonly=True, default=lambda self: self._context.get('order_id'))
    price = fields.Float(u'应付金额', readonly=True, default=lambda self: self._context.get('price'))
    recept_money = fields.Float(u'收款金额', required=True)
    change_money = fields.Float(u'找零', compute='_computer_change_money')

    @api.multi
    @api.depends('recept_money')
    def _computer_change_money(self):
        for m in self:
            m.change_money = m.recept_money - m.price

    @api.multi
    @api.constrains('recept_money')
    def _check_payment(self):
        for m in self:
            if m.recept_money < m.price:
                raise ValidationError(u'收款金额不能小于应付金额.')

    @api.multi
    def pay(self):

        order = self.env['zndx.order'].browse(self._context.get('order_id'))
        if order:
            order.write({'payment': self.price, 'state': u'已付款'})
        return {}
