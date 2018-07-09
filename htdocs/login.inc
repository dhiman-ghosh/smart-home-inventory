<div class="login-form">    
  <form action="/auth" method="post">
    <div class="avatar"><i class="material-icons">&#xE7FF;</i></div>
      <h4 class="modal-title">Login to Your Account</h4>
        <div class="form-group">
          <input type="password" name="pin" class="form-control" placeholder="Enter Access Key" pattern="[0-9]{6}" title="Enter 6 digit numeric PIN" required="required">
          {% if error>0 %}
          <div class="text-danger">Invalid access code!</div>
          {% endif %}
        </div>
        <div class="form-group small clearfix">
          <label class="checkbox-inline"><input type="checkbox"> Remember me</label>
          <a href="#" class="forgot-link" data-toggle="tooltip" 
            title="It is the 6 digit PIN provided by your alexa device for accessing your account">What is access key?</a>
        </div> 
        <input type="submit" class="btn btn-primary btn-block btn-lg" value="Login">              
    </form>     
  <div class="text-center small">
    Don't have an access key? <br />
    Say <i><a href="#">Alexa, ask inventory to tell my access key</a></i>
  </div>
</div>
