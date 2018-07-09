<div class="login-form">    
  <form action="/api/v1/stock/{{barcode}}" id="stock" method="post">
    <div class="avatar"><i class="material-icons">&#xE02E;</i></div>
      <h4 class="modal-title">Amul Lassi</h4>
      <div class="text-center">
        <button type="button" class="btn-info btn-lg">100 ml</button>
        <button type="button" class="btn-info btn-lg">2 Qty</button>
        <button type="button" class="btn-info btn-lg">15 INR</button>
      </div>
      <br/>
        <div class="form-group">
          <input type="text" name="barcode" class="form-control" disabled>
          <input type="hidden" id="action" name="action" value="add">
          <input type="number" name="quantity" value="1" class="form-control" placeholder="Quantity" required="required">
        </div>
        <input type="submit" class="btn-success btn-block btn-lg" value="Add">
        <button type="button" id="remove" class="btn-danger btn-block btn-lg">Remove</button>
    </form>     
  <div class="text-center small">
    Want to update product info? <i><a href="#">Click here</a></i>
  </div>
</div>

<script>
$('button#remove').click( function() {
  $('input#action').val('remove');
  $('form#stock').submit()
});
</script>
