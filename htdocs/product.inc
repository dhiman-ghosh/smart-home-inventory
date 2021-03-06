{% if data is defined %}
{% set company = data['brand'] %}
{% set name = data['name'] %}
{% set category = data['category'] %}
{% set price = data['mrp'] %}
{% set measurement = data['measurement'] %}
{% set stock = data['stock'] %}
{% else %}
{% set company = '' %}
{% set name = '' %}
{% set category = '' %}
{% set price = '' %}
{% set measurement = '' %}
{% set stock = '0' %}
{% endif %}

<div class="login-form">    
  <form id="api" action="/api/v1/product/{{action}}" method="post">
    <div class="avatar"><i class="material-icons">&#xE02E;</i></div>
      <h4 class="modal-title">Add / Update Product</h4>
        <div class="form-group">
          <input type="text" name="barcode" class="form-control" value="{{barcode}}" disabled>
          <input type="text" name="company" class="form-control" placeholder="Company Name" value="{{company}}"required="required">
          <input type="text" name="name" class="form-control" placeholder="Product Name" value="{{name}}" required="required">
          <select class="form-control" id="category" placeholder="Product Category" name="category">
            <option value="biscuits">Biscuits</option>
            <option value="noodles">Noodles</option>
            <option value="spices">Spices</option>
            <option value="grocery">Grocery</option>
            <option value="foods">Foods</option>
            <option value="drinks">Drinks</option>
            <option value="medicine">Medicine</option>
            <option value="stationary">Stationary</option>
            <option value="sanitary">Sanitary</option>
            <option value="water">Water</option>
            <option value="others">Others</option>
          </select>
          <input type="text" name="measurement" class="form-control" placeholder="Measurement" value="{{measurement}}" required="required">
          <input type="text" name="mrp" class="form-control" placeholder="MRP in INR" value="{{price}}" required="required">
          <input type="hidden" name="stock" class="form-control" value="{{stock}}">
        </div>
        <input type="submit" class="btn btn-primary btn-block btn-lg" value="Confirm">              
        <input type="button" id="cancel" class="btn btn-primary btn-block btn-lg" value="Cancel">
    </form>     
  <div class="text-center small">
    Product already updated? <i><a href="#">Click here to update stock</a></i>
  </div>
</div>
<script>
  $('select#category').val('{{category}}');
</script>
