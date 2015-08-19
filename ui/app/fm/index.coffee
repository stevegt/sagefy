h = require('virtual-dom/h')

{init, store, broker} = require('./framework')



store.add({
    open: (href) ->
        console.log(href)
})





render = (data) ->
    return (
        h('div'
            {className: 'foo'}
            h('a'
                {href: 'http://google.com'}
                'Google'
            )
        )
    )
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

actions = store.actions

broker.add({
    'click .foo a': (e, el) ->
        e.preventDefault()
        actions.open(el.href)
})





init({
    el: document.body
    view: render
})