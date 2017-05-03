const {div, h1, h3, a, p, hr, ul, li} = require('../../modules/tags')
const {unitWizard} = require('./create_shared.fn')
const icon = require('../components/icon.tmpl')
const previewUnitHead = require('../components/preview_unit_head.tmpl')

module.exports = function createUnitList(data) {
    const {units} = data.create
    const selectedSet = data.create.selectedSet || {}
    const setName = selectedSet.name || '???'

    return div(
        {id: 'create', className: 'page create--unit-list'},
        h1('Add Units to Set'),
        unitWizard('list'),

        h3(`Create and Add Units for ${setName}`),

        // TODO List of existing units (if any)

        units && units.length ? ul(
            {className: 'create--unit-list__units'},
            units.map((unit, index) => li(
                a(
                    {
                        dataset: {index},
                        href: '#',
                        className: 'create--unit-list__remove'
                    },
                    icon('remove'),
                    ' Remove'
                ),
                previewUnitHead({
                    name: unit.name,
                    body: unit.body,
                })
            ))
        ) : p('No units added yet.'),

        a(
            {
                className: 'create--unit-list__create',
                href: '/create/unit/create',
            },
            icon('create'),
            ' Create a New Unit'
        ),
        a(
            {
                className: 'create--unit-list__add',
                href: '/create/unit/add',
            },
            icon('search'),
            ' Add an Existing Unit'
        ),

        hr(),

        a(
            {
                href: '#',
                className: 'create--unit-list__submit'
            },
            icon('create'),
            ' Submit This Work'
        ),
        a(
            {
                href: '/create',
                className: 'create__home',
            },
            icon('back'),
            ' Return to Create Overview'
        )
    )
}
