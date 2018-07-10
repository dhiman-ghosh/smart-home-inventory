{% if data is defined %}
{% set name = data['name'] %}
{% set email = data['email'] %}
{% set phone = data['phone'] %}
{% else %}
{% set name = '' %}
{% set email = '' %}
{% set phone = '' %}
{% endif %}

<div class="login-form">    
  <form action="/api/v1/profile/{{key}}" method="post">
    <div class="avatar"><i class="material-icons">&#xE7FF;</i></div>
      <h4 class="modal-title">Update User Profile</h4>
        <div class="form-group">
          <input type="text" name="name" class="form-control" placeholder="Full Name" value="{{name}}" disabled>
          <input type="text" name="email" class="form-control" placeholder="Email Address" value="{{email}}"required="required">
          <input type="text" name="phone" class="form-control" placeholder="Mobile Number" value="{{phone}}" required="required">
        </div>
        <input type="submit" class="btn btn-primary btn-block btn-lg" value="Update">              
    </form>     
  <div class="text-center small">
    Profile already updated? <i><a href="./">Click here to go to home</a></i>
  </div>
</div>
