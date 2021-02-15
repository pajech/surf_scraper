const knex = require('knex')(require('./knexfile'))

module.exports = {
    createUser ({ username, phonenumber }) {
      console.log(`Add user ${username} with phonenumber ${phonenumber}`)
      return knex('user').insert({
        username,
        phonenumber
      })
    }
  }


