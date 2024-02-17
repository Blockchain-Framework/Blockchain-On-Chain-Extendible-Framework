function CustomTree {
    param(
        [string]$startDirectory = ".",
        [string[]]$excludeDirs = @("venv", "__pycache__") # Now supports multiple directories
    )

    $indent = "    "
    $stack = New-Object System.Collections.Stack

    $stack.Push((Get-Item $startDirectory))

    while ($stack.Count -gt 0) {
        $dir = $stack.Pop()
        $level = ($dir.FullName.Split("\").Count - $startDirectory.Split("\").Count)
        $indentation = $indent * $level
        Write-Host "$indentation$(Split-Path $dir -Leaf)/"

        $children = Get-ChildItem $dir.FullName | Where-Object { 
            $_.PSIsContainer -and $excludeDirs -notcontains $_.Name 
        } | Sort-Object { $_.PSIsContainer } -Descending
        foreach ($child in $children) {
            $stack.Push($child)
        }

        $files = Get-ChildItem $dir.FullName | Where-Object { -not $_.PSIsContainer }
        foreach ($file in $files) {
            Write-Host "$indentation$indent$file"
        }
    }
}

# Usage example
CustomTree -startDirectory "D:\Academics\FYP\Repos_new_new\Blockchain-On-Chain-Extendible-Framework" -excludeDirs @("venv", "__pycache__")
