const CreateUser = document.querySelector('.CreateUser')
CreateUser.addEventListener('submit', (e) => {
  e.preventDefault()
  const username = CreateUser.querySelector('.username').value
  const phonenumber = CreateUser.querySelector('.phonenumber').value
  post('/createUser', { username, phonenumber })
})

function post (path, data) {
    return window.fetch(path, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
  }