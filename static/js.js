$(document).ready(function(){
  $("#ModalQtd, #ModalPreco").change(function(){
    valor_atual = $("#preco_compra").val()
    valor_novo = $("#ModalPreco").val()
    calculo = ((valor_novo - valor_atual) / valor_atual) * 100
    if (calculo < 0){
      $("#ModalNome").removeClass("text-success");
      $("#ModalNome").addClass("text-danger");
      $("#resolved-symbol-modalvender").removeClass("fa-up-long");
      $("#resolved-symbol-modalvender").addClass("fa-down-long text-danger") 
    }else{
      $("#ModalNome").removeClass("text-danger");
      $("#ModalNome").addClass("text-success");
      $("#resolved-symbol-modalvender").removeClass("fa-down-long text-danger");
      $("#resolved-symbol-modalvender").addClass("fa-up-long text-success") 
    }
    $("#up").text(calculo.toFixed(2))
  });

  $("#select-tipo-editar").change(function(){
    switch($(this).val()) {
      case "entrada":
        $('#select-categoria-editar').empty();
        $('#select-categoria-editar').append('<option value="salario">Salario</option>');
        $('#select-categoria-editar').append('<option value="venda de servico">Venda de servico</option>');
        $('#select-categoria-editar').append('<option value="venda de produto">Venda de produto</option>');
        $("#quantidade-editar input").val(1);
        $("#quantidade-editar input").attr({"max": "1", "min": "1"});
        break;
      case "saida":
        $('#select-categoria-editar').empty();
        $('#select-categoria-editar').append('<option value="compra">Compra</option>');
        $("#quantidade-editar input").val(1);
        $("#quantidade-editar input").attr({"max": "1", "min": "1"});
        break;
      case "investimento":
        $('#select-categoria-editar').empty();
        $('#select-categoria-editar').append('<option value="renda fixa">Renda fixa</option>');
        $('#select-categoria-editar').append('<option value="renda variavel">Renda variavel</option>');
        $('#select-categoria-editar').append('<option value="fii">FII</option>');
        $('#select-categoria-editar').append('<option value="etf">ETF</option>');
        $('#select-categoria-editar').append('<option value="brd">BRD</option>');
        $('#select-categoria-editar').append('<option value="criptomoedas">Criptomoedas</option>');
        $("#quantidade-editar input").removeAttr("max");
    }
  });
  if ($("#select-tipo-editar").val() == "investimento"){
    $("#quantidade-editar").prop("disabled", false);
  }
  
});

// funcao setar no modal/ onclick
// funcao calcular

var data = new Date();
var dia = String(data.getDate()).padStart(2, '0');
var mes = String(data.getMonth() + 1).padStart(2, '0');
var ano = data.getFullYear();
dataAtual = ano + '-' + mes + '-' + dia;

function VenderModal(nome, quantidade, preco, id){
  $("#ModalNome").html(nome);
  $("#ModalQtd").val(quantidade);
  $("#ModalPreco").val(preco);
  $('#modalvender').modal('show');
  $('#data-venda').val(dataAtual)
  $("#ModalQtd").attr({"max" : quantidade, "mix" : 1.0});

  $("#id_vender_modal").val(id);
  $("#nome_venda").val(nome);
  $("#preco_compra").val(preco);

  valor_atual = preco
  valor_novo = $("#ModalPreco").val()

  calculo = ((valor_novo - valor_atual) / valor_atual) * 100
  if (calculo < 0){
    $("#resolved-symbol-modalvender").removeClass("fa-up-long");
    $("#resolved-symbol-modalvender").addClass("fa-down-long text-danger") 
  }else{
    $("#resolved-symbol-modalvender").removeClass("fa-down-long text-danger");
    $("#resolved-symbol-modalvender").addClass("fa-up-long text-success") 
  }
    $("#up").text(calculo.toFixed(2))
}
function TipoCategoriaEditar(tipo, categoria){
  switch(tipo) {
    case "entrada":
      $("#select-categoria-editar option[value='entrada'").prop("selected", true);
      $('#select-categoria-editar').empty();
      $('#select-categoria-editar').append('<option value="salario">Salario</option>');
      $('#select-categoria-editar').append('<option value="venda de servico">Venda de servico</option>');
      $('#select-categoria-editar').append('<option value="venda de produto">Venda de produto</option>');
      $("#quantidade-editar input").val(1);
      $("#quantidade-editar input").attr({"max": "1", "min": "1"});
      break;
    case "saida":
      $("#select-categoria-editar option[value='saida']").prop("selected", true);
      $('#select-categoria-editar').empty();
      $('#select-categoria-editar').append('<option value="compra">Compra</option>');
      $("#quantidade-editar input").val(1);
      $("#quantidade-editar input").attr({"max": "1", "min": "1"});
      break;
    case "investimento":
      $("#select-categoria-editar option[value='investimento']").prop("selected", true);
      $('#select-categoria-editar').empty();
      $('#select-categoria-editar').append('<option value="renda fixa">Renda fixa</option>');
      $('#select-categoria-editar').append('<option value="renda variavel">Renda variavel</option>');
      $('#select-categoria-editar').append('<option value="fii">FII</option>');
      $('#select-categoria-editar').append('<option value="etf">ETF</option>');
      $('#select-categoria-editar').append('<option value="brd">BRD</option>');
      $('#select-categoria-editar').append('<option value="criptomoedas">Criptomoedas</option>');
      $("#quantidade-editar input").removeAttr("max", "min");
  }
}
