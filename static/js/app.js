var QRList = React.createClass({
  render: function() {
    var createItem = function(itemText, index) {
      return <li key={index + itemText}>
        <img src={"/static/images/" + (index + 1) + ".jpg"} alt="qrcode" />
        {itemText}
      </li>;
    };
    return <ol>{this.props.items.map(createItem)}</ol>;
  }
});

var QRApp = React.createClass({
  getInitialState: function() {
    return {items: [], text: ''};
  },
  onChange: function(e) {
    this.setState({text: e.target.value});
  },
  handleSubmit: function(e) {
    e.preventDefault();
    if (this.state.text != "") {
      var nextItems = this.state.items.concat([this.state.text]);
      var nextText = '';
      this.setState({items: nextItems, text: nextText});
      this.generateQR();
    };
  },
  generateQR: function() {
   $.ajax({
    url: "/add.json",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({'len': this.state.items.length + 1, 'text': this.state.text}),
    dataType: 'json',
    cache: false,
    success: function() {
      console.log("Успешное выполнение");
    }.bind(this),
    error: function(xhr, status, err) {
      console.error("add.json", status, err.toString());
    }.bind(this)
  });
  },
  render: function() {
    return (
      <div>
        <h3>QR code генератор</h3>
        <form onSubmit={this.handleSubmit}>
          <input onChange={this.onChange} value={this.state.text} />
          <button>{'Создать #' + (this.state.items.length + 1)}</button>
        </form>
        <QRList items={this.state.items} />
      </div>
    );
  }
});

React.render(<QRApp />, document.getElementById('content'));