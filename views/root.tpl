<!doctype html>
<html lang="en">

<head>
  <title>{{ title }}</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,height=device-height,initial-scale=1">
  <link href="./css/common.css" rel="stylesheet">
</head>

<body>
  <h1>{{ title }}</h1>
  <form action="./query" method="POST">
    <input name="url" type="url" placeholder="URL" aria-label="URL" aria-describedby="button-submit" required autofocus>
    <select name="format">
      <optgroup label="Video">
        % for item in format_list['video']:
        <option value="{{ item['value'] }}">{{ item['text'] }}</option>
        % end
      </optgroup>
      <optgroup label="Audio">
        % for item in format_list['audio']:
        <option value="{{ item['value'] }}">{{ item['text'] }}</option>
        % end
      </optgroup>
    </select>
    <button type="submit" id="button-submit">Submit</button>
  </form>
</body>

</html>