@echo off
setlocal

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"$names = @('DataSchool Check-in','DataSchool Mid-Attendance','DataSchool Check-out'); ^
Write-Host 'DataSchool scheduled tasks'; ^
Write-Host '----------------------------------------'; ^
foreach ($name in $names) { ^
  $task = Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue; ^
  if ($null -eq $task) { ^
    Write-Host ($name + ' : NOT FOUND'); ^
  } else { ^
    $info = Get-ScheduledTaskInfo -TaskName $name; ^
    $trigger = @($task.Triggers)[0]; ^
    if ($trigger -and $trigger.StartBoundary) { $start = ([datetime]$trigger.StartBoundary).ToString('HH:mm') } else { $start = '-' }; ^
    if ($info.NextRunTime) { $next = $info.NextRunTime.ToString('yyyy-MM-dd HH:mm') } else { $next = '-' }; ^
    Write-Host ($name + ' | Start=' + $start + ' | Next=' + $next + ' | State=' + $task.State); ^
  } ^
}"

pause
