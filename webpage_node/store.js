module.exports = {
    createUser ({ username, phonenumber }) {
      console.log(`Add user ${username} with phonenumber ${phonenumber}`)
      return Promise.resolve()
    }
  }