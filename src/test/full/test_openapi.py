import schemathesis

schema = schemathesis.from_uri("https://127.0.0.1:8000/openapi.json")
schemathesis.experimental.OPEN_API_3_1.enable()


@schema.parametrize()
def test_api(case):
    case.call_and_validate()
