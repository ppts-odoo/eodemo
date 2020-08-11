from odoo import fields, models, api, _

class EventEvent(models.Model):
    _inherit = "event.event"

    def button_confirm(self):
        event = super(EventEvent, self).button_confirm()
        self.env['calendar.event'].create({
            'name':self.name,
            'start':self.date_begin,
            'stop':self.date_end,
            'event_id':self.id,
            'location':self.address_id.city,
            'description':self.name,
        })
        return event

    def unlink(self):
        calendar = self.env['calendar.event'].sudo().search([('event_id','=',self.id)])
        if calendar:
            calendar.unlink()
        return super(EventEvent, self).unlink()

    def open_related_calendars(self):
        return {
            'name': _('Calendar'),
            'view_mode': 'tree,form',
            'res_model': 'calendar.event',
            'view_id': False,
            'views': [(self.env.ref('calendar.view_calendar_event_tree').id, 'tree'),
                      (self.env.ref('calendar.view_calendar_event_form').id, 'form')],
            'type': 'ir.actions.act_window',
            'domain': [('event_id', '=', self.id)],
            'context': {'create': False},
        }


class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.model
    def create(self, vals):
        res = super(EventRegistration, self).create(vals)
        if 'from_event' not in self.env.context:
            if res:
                partner_id = self.env['res.partner'].sudo().search([('email', '=',res.email)],limit=1)
                if partner_id:
                    calendar = self.env['calendar.event'].sudo().search([('event_id', '=', res.event_id.id)])
                    if calendar:
                        calendar.sudo().write({'partner_ids': [(4, partner_id.id)]})
                else:
                    partner_id = self.env['res.partner'].sudo().create({'name':res.name, 'email':res.email, 'phone':res.phone})
                    if partner_id:
                        calendar = self.env['calendar.event'].sudo().search([('event_id','=',res.event_id.id)])
                        if calendar:
                            calendar.sudo().with_context(from_registration=True).write({'partner_ids':[(4,partner_id.id)]})
        return res




