{% if data is defined %}
{% set company = data['company'] %}
{% set name = data['name'] %}
{% set category = data['category'] %}
{% set price = data['price'] %}
{% set measurement = data['measurement'] %}
{% else %}
{% set company = '' %}
{% set name = '' %}
{% set category = '' %}
{% set price = '' %}
{% set measurement = '' %}
{% endif %}

<div class="login-form">    
  <form action="/api/v1/product/{{action}}" method="post">
    <div class="avatar"><i class="material-icons">&#xE02E;</i></div>
      <h4 class="modal-title">Add / Update Product</h4>
        <div class="form-group">
          <input type="text" name="barcode" class="form-control" value="{{barcode}}" disabled>
          <input type="text" name="company" class="form-control" placeholder="Company Name" value="{{company}}"required="required">
          <input type="text" name="name" class="form-control" placeholder="Product Name" value="{{name}}" required="required">
          <input type="text" name="category" class="form-control" placeholder="Product Category" value="{{category}}" required="required">
          <input type="text" name="measurement" class="form-control" placeholder="Measurement" value="{{measurement}}" required="required">
          <input type="text" name="mrp" class="form-control" placeholder="MRP in INR" value="{{price}}" required="required">
          <input type="hidden" name="redirect" value="true">
        </div>
        <input type="submit" class="btn btn-primary btn-block btn-lg" value="Confirm">              
    </form>     
  <div class="text-center small">
    Product already updated? <i><a href="#">Click here to update stock</a></i>
  </div>
</div>
