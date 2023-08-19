from datetime import datetime


class NewLineRequest:
    """
    POST /order-item neither returns an order-item object or its ID. With this
    class, we aim to present a partially reconstructed order item based on the
    input parameters, using the few matching parameters between the response
    of GET /order-item/:id and the request of POST /order-item.
    The specification doesn't explicitly state the optimistic equivalence presented
    here, so this mapping needs to be reviewed later on.
    """

    def __init__(self, new_order_item, account_id):
        self.lineInfos = new_order_item["lineInfo"]
        self.account_id = account_id

    def to_order_item(self):
        """
        Maps the atttributes of a NewLineRequest instance, as specified in Swagger,
        to the attributes of an OrderItem instance, as specified in a GET response.

        :return: dict
        """

        order_item_list = []
        for line in self.lineInfos:
            order_item_dct = {
                "account_id": self.account_id,
                "name": line.get("name"),
                "surname": line.get("surname"),
                "phone": line.get("phoneNumber"),
                "orderType": "OrderItem",
                "status": "Esperando para enviar",
                "productName": "Unknown",
                "createdDate": datetime.now(),
                "lastModifiedDate": datetime.now(),
                "attributes": {
                    "Nombre": line.get("name"),
                    "Apellidos": line.get("surname"),
                    "ICCID_Donante": line.get("iccid_donante"),
                    "Tipo_de_Documento": line.get("documentType"),
                    "Numero_de_Documento": line.get("docid"),
                    "Operador_Donante_Movil": line.get("donorOperator"),
                    "Operador_Receptor_Movil": "Som Connexió",
                    "Fecha_de_solicitud_del_abonado": datetime.now(),
                },
                "simAttributes": {
                    "ICCID": line.get("iccid"),
                },
            }
            order_item_list.append(order_item_dct)

        return order_item_list
