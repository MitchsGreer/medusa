# Chore Format

This is the format each chore must follow to be read into Medusa. This
information is stored in a JSON file, marked y the `.json` extension.

## Format

```json
{
  "name": "<CHORE_NAME>",
  "location": "<CHORE_LOCATION>",
  "description": "<CHORE_DESCRIPTION>",
  "frequency": "<CHORE_FREQUENCY>",
  "delta": "<CHORE_PROBABILITY_DELTA>",
  "type": "<CHORE_TYPE>",
  "last_completed": "<DATE_LAST_COMPLETED>"
}
```

| Name                    | Description                                                                                                      | Type  |
| :---------------------- | :--------------------------------------------------------------------------------------------------------------- | :---- |
| CHORE_NAME              | The name of the chore.                                                                                           | `str` |
| CHORE_LOCATION          | The room or specific location the chore takes place in.                                                          | `str` |
| CHORE_DESCRIPTION       | The description of what the chore is.                                                                            | `str` |
| CHORE_FREQUENCY         | The frequency in days the chore should be done.                                                                  | `int` |
| CHORE_PROBABILITY_DELTA | The amount of time after the chore has been marked as `TODO` to increase the draw probability in the chore draw. | `int` |
| CHORE_TYPE              | The type of chore, `weekend` or `weekday`.                                                                       | `str` |
| DATE_LAST_COMPLETED     | The date the chore was last completed.                                                                           | `str` |
