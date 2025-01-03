# Chore Pot

The chore pot is a grouping of chores that could be drawn for today. Chores can
be added multiple time depending on how long it has been since they were last
completed. A chore is added based on the following calculation.

```
(days(today - last_done) // delta) + 1
```

This is done after the frequency has been met and will only add days for of the
type of that day. Weekdays being Monday though Friday and weekends being Sunday
and Saturday.
