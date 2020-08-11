from odoo import fields, models, api, _

class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    event_id = fields.Many2one('event.event', 'Event')

    def write(self, vals):
        if 'from_registration' not in self.env.context:
            if self.event_id:
                if vals.get('stop'):
                    self.event_id.write({'date_end': vals.get('stop')})
                if vals.get('start'):
                    self.event_id.write({'date_begin': vals.get('start')})
                if vals.get('partner_ids'):
                    for record in vals.get('partner_ids')[0][2]:
                        partner_id=self.env['res.partner'].browse(record)
                        if partner_id:
                            event_registration = self.env['event.registration'].search([('email', '=',partner_id.email),('event_id', '=',self.event_id.id)],limit=1)
                            if not event_registration:
                                self.env['event.registration'].with_context(from_event=True).create({'name':partner_id.name, 'email':partner_id.email,'phone':partner_id.phone,'event_id':self.event_id.id})
        return super(CalendarEvent, self).write(vals)