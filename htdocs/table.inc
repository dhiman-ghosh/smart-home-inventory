<!--Table-->
<div class="table-responsive">
<table class="table table-striped">

  <!--Table head-->
    <thead>
      <tr>
        <th>Barcode Number</th>
        <th>Company</th>
        <th>Name</th>
        <th>Price</th>
        <th>Stock</th>
        <th>Movement</th>
      </tr>
    </thead>
  <!--Table head-->

  <!--Table body-->
  <tbody>
  {% for key, value in data.items() %}
         
    <tr>
      <th scope="row"> {{ key }} </th>
      <td> {{ value[0] }} </td>
      <td> {{ value[1] }} </td>
      <td> {{ value[2] }} </td>
      <td> {{ value[3] }} </td>
      <td> {{ value[4] }} </td>
    </tr>
            
  {% endfor %} 
  <!--Table body-->

</table>
<!--Table-->
</div>
<a href="/logout" class="btn btn-link" role="button">Sign out</a>
