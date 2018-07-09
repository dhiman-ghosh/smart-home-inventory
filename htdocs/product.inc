<div class="login-form">    
  <form action="/product" method="post">
    <div class="avatar"><i class="material-icons">&#xE02E;</i></div>
      <h4 class="modal-title">Add / Update Product</h4>
        <div class="form-group">
          <input type="text" name="barcode" class="form-control" disabled>
          <input type="text" name="company" class="form-control" placeholder="Company Name" required="required">
          <input type="text" name="name" class="form-control" placeholder="Product Name" required="required">
          <input type="text" name="category" class="form-control" placeholder="Product Category" required="required">
          <input type="text" name="measurement" class="form-control" placeholder="Measurement" required="required">
          <input type="text" name="mrp" class="form-control" placeholder="MRP in INR" required="required">
        </div>
        <input type="submit" class="btn btn-primary btn-block btn-lg" value="Confirm">              
    </form>     
  <div class="text-center small">
    Product already updated? <i><a href="#">Click here to update stock</a></i>
  </div>
</div>
