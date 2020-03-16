
async def test_index(cli):
    response = await cli.get('/')
    assert response.status == 200
    text = await response.text()
    assert '200: OK' in text


async def test_load_success_1(cli):
    response = await cli.post('/load', json={"words": "foobar"})
    assert response.status == 200
    text = await response.text()
    assert '200: OK' in text


async def test_load_success_2(cli):
    data = {"words": ["foobar", "aabb", "baba", "boofar", "test", "foobar"]}
    response = await cli.post('/load', json=data)
    assert response.status == 200
    text = await response.text()
    assert '200: OK' in text


async def test_load_failed_1(cli):
    response = await cli.post('/load')
    assert response.status == 422
    _json = await response.json()
    assert _json == {"words": ["Missing data for required field."]}


async def test_load_failed_2(cli):
    response = await cli.post('/load', json={"words": ["foobar", 1]})
    assert response.status == 422
    _json = await response.json()
    assert _json == {"words": {"1": ["Not a valid string."]}}


async def test_load_failed_3(cli):
    response = await cli.post('/load', json={"words": []})
    assert response.status == 422
    _json = await response.json()
    assert _json == {"words": ["Length must be between 1 and 100."]}


async def test_get_success_1(cli):
    response = await cli.get('/get')
    assert response.status == 200
    text = await response.text()
    assert text == 'null'


async def test_get_success_2(cli):
    response = await cli.get('/get?word=foobar')
    assert response.status == 200
    _json = await response.json()
    assert sorted(_json) == ["boofar", "foobar"]


async def test_get_success_3(cli):
    response = await cli.get('/get?word=foobar&key=value')
    assert response.status == 200
    _json = await response.json()
    assert sorted(_json) == ["boofar", "foobar"]


async def test_get_success_4(cli):
    response = await cli.get('/get?key=value')
    assert response.status == 200
    text = await response.text()
    assert text == 'null'
