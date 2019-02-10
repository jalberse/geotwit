if ( isset( $_POST['submit'] ) ) {
  $message = $_POST['message'];
  echo '<h3>Form POST Method</h3>'; echo 'Your phrases are ' . $message; exit;
}
