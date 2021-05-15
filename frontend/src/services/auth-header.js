export default function auth_header() {
    var user = JSON.parse(localStorage.getItem('user'));
    try {
      var headers = {
        'Content-Type' : 'application/json',
        'Accept' : 'application/json',
        'Authorization' : `Bearer ${user.access}`
      }
      return headers
    } catch (error) {
      return {};
    }

}