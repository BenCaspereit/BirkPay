test('halbe UID zeigt Fehler', async ({ page }) => {
  await page.goto('/')
  // Öffne z.B. erst das Modal oder simuliere den Klick auf "Jetzt Abbuchen"
  await page.click('button:has-text("Jetzt Abbuchen")')
  
  await page.keyboard.type('04A1', { delay: 5 })   // Kein Enter -> Timeout greift
  
  // Text an dein Composable angepasst:
  await expect(page.getByText(/Übertragung unvollständig/)).toBeVisible()
})